from rest_framework.exceptions import ValidationError
from sacco.serializers import MatatuSerializer

def test_registration_number_validation():
    # Data with an invalid registration number
    serializer = MatatuSerializer(data={'registration_number': '123!@#'})
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        # Assert that the correct validation error message is raised
        assert "Registration number must be alphanumeric" in str(e)
