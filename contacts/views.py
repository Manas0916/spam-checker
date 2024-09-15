from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer, DetailedUserSerializer, DetailedContactSerializer

class UserRegisterView(generics.CreateAPIView):
    """
    API view for registering a new user.

    This view allows any user to register by providing their details.
    The user's details are validated using the `UserSerializer` serializer.

    Attributes:
        permission_classes (list): A list of permission classes applied to this view.
            In this case, the `AllowAny` class is used, allowing any user to access this view.
        queryset (QuerySet): The queryset used to retrieve the list of users.
            In this case, all users are retrieved using the `User.objects.all()` method.
        serializer_class (Serializer): The serializer class used to validate and serialize user data.
            In this case, the `UserSerializer` class is used.

    Methods:
        post(request): Handles the HTTP POST request to register a new user.
            This method validates the user's data, creates a new user object, and returns the response.
    """
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    """
    API view for user login.

    This view allows users to authenticate and login using their username and password.
    The `post` method handles the login request and returns a response indicating whether
    the login was successful or not.
    Methods:
        post(request): Handles the login request and returns a response.

    Attributes:
        permission_classes (list): A list of permission classes applied to the view.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Handles the login request and returns a response.
        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the login result.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ContactListView(generics.ListCreateAPIView):
    """
    API view for listing and creating contacts.

    Inherits from `generics.ListCreateAPIView` which provides
    the implementation for GET and POST methods.

    Attributes:
        serializer_class (class): The serializer class to use for
            serializing and deserializing contact data.
        permission_classes (list): The list of permission classes
            that the view requires for authentication.
    Methods:
        get_queryset(): Returns the queryset of contacts filtered
            by the current user.
        perform_create(serializer): Performs the creation of a new
            contact and associates it with the current user.
    """

    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of contacts filtered by the current user.

        Returns:
            QuerySet: The queryset of contacts filtered by the current user.
        """
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Performs the creation of a new contact and associates it with the current user.

        Args:
            serializer (Serializer): The serializer instance used for deserialization.

        Returns:
            None
        """
        serializer.save(owner=self.request.user)

class MarkSpamView(APIView):
    """
    API view to mark a phone number as spam.

    Requires authentication.

    Parameters:
    - request: The HTTP request object.
    - phone_number: The phone number to mark as spam.

    Returns:
    - If the phone number exists in the contacts, it is marked as spam and a success message is returned.
    - If the phone number does not exist in the contacts, an error message is returned with a 404 status code.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, phone_number):
        contacts = Contact.objects.filter(phone_number=phone_number)
        if contacts.exists():
            contacts.update(is_spam=True)
            return Response({'message': 'Number marked as spam'})
        return Response({'error': 'Number not found'}, status=status.HTTP_404_NOT_FOUND)

class CheckSpamView(APIView):
    """
    API view to check if a phone number is marked as spam.

    Requires authentication.

    Parameters:
    - request: The HTTP request object.
    - phone_number: The phone number to check.

    Returns:
    - If the phone number exists in the contacts and is marked as spam, it returns a response indicating that the number is spam.
    - If the phone number exists in the contacts but is not marked as spam, it returns a response indicating that the number is not spam.
    - If the phone number does not exist in the contacts, it returns a response indicating that the number is not found.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        """
        Handles the GET request to check if a phone number is marked as spam.

        Parameters:
            request (Request): The HTTP request object.
            phone_number (str): The phone number to check.

        Returns:
            Response: The HTTP response object containing the result of the spam check.
        """
        is_spam = Contact.objects.filter(phone_number=phone_number, is_spam=True).exists()
        return Response({'phone_number': phone_number, 'is_spam': is_spam})

class SearchView(APIView):
    """
    API view for searching users and contacts based on query parameters.

    Supported query parameters:
    - search_by: Specifies the field to search by (name or phone)
    - query: The search query

    Returns a list of search results, including user and contact information.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests for searching users and contacts.

        Returns:
        - If successful, returns a list of search results.
        - If query parameter is missing, returns a 400 Bad Request response.
        - If search_by parameter is invalid, returns a 400 Bad Request response.
        """

        search_by = request.query_params.get('search_by', 'name')
        query = request.query_params.get('query')
        
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        if search_by == 'name':
            users = User.objects.filter(username__icontains=query)
            contacts = Contact.objects.filter(name__icontains=query)
        elif search_by == 'phone':
            users = User.objects.filter(phone_number=query)
            contacts = Contact.objects.filter(phone_number=query)
        else:
            return Response({'error': 'Invalid search_by parameter'}, status=status.HTTP_400_BAD_REQUEST)

        user_results = self._get_user_results(users, query)
        contact_results = self._get_contact_results(contacts)

        results = user_results + contact_results
        results = self._sort_results(results, query)
        
        return Response(results)

    def _get_user_results(self, users, query):
        """
        Retrieves search results for users based on the given query.

        Args:
        - users: QuerySet of User objects
        - query: The search query

        Returns:
        - A list of user search results, including name, phone number, and spam status.
        """

        user_results = []
        for user in users:
            user_result = {
                'name': user.username,
                'phone_number': user.phone_number,
                'is_spam': Contact.objects.filter(phone_number=user.phone_number, is_spam=True).exists()
            }
            user_results.append(user_result)
        return user_results

    def _get_contact_results(self, contacts):
        """
        Retrieves search results for contacts based on the given query.

        Args:
        - contacts: QuerySet of Contact objects

        Returns:
        - A list of contact search results, including name, phone number, and spam status.
        """

        contact_results = []
        for contact in contacts:
            contact_result = {
                'name': contact.name,
                'phone_number': contact.phone_number,
                'is_spam': contact.is_spam
            }
            contact_results.append(contact_result)
        return contact_results

    def _sort_results(self, results, query):
        """
        Sorts the search results based on the given query.

        Args:
        - results: List of search results
        - query: The search query

        Returns:
        - The sorted list of search results.
        """

        results = sorted(results, key=lambda x: (x['name'].startswith(query), query in x['name']), reverse=True)
        return results
    
    
class DetailedSearchView(APIView):
    """
    API view for detailed search of users and contacts based on phone number.
     Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, phone_number):
        """
        Retrieve detailed information about a user or contacts based on the provided phone number.

        Args:
            request (HttpRequest): The HTTP request object.
            phone_number (str): The phone number to search for.

        Returns:
            Response: The response containing the serialized data of the user or contacts.
            The person email is only displayed if the person is a registered user 
            and the user who is searching is in the person contact list.

        Raises:
            User.DoesNotExist: If no user with the provided phone number is found.
        """

        try:
            user = User.objects.get(phone_number=phone_number)
            serializer = DetailedUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except User.DoesNotExist:
            contacts = Contact.objects.filter(phone_number=phone_number)
            if contacts.exists():
                serializer = DetailedContactSerializer(contacts, many=True, context={'request': request})
                return Response(serializer.data)
            return Response({'error': 'User or Contact not found'}, status=status.HTTP_404_NOT_FOUND)
