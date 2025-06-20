from rest_framework import serializers

from book.models import Book
from .models import Loan
from book.serializers import BookSerializer
from user.serializers import UserSerializer


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = '__all__'

class LoanSerializerForUser(serializers.ModelSerializer):
    loanDate = serializers.SerializerMethodField()
    expireDate = serializers.SerializerMethodField()
    bookName = serializers.SerializerMethodField()
    returnDate = serializers.SerializerMethodField()

    def get_expireDate(self,obj):
        expdate= str(obj.expireDate)
        return expdate[0:10]

    def get_returnDate(self,obj):
        if obj.returnDate:
            expdate= str(obj.returnDate)
            return expdate[0:10]
        else:
            return None

    def get_loanDate(self,obj):
        expdate = str(obj.loanDate)
        return expdate[0:10]

    def get_bookName(self,obj):
        book = Book.objects.get(id=obj.book.id)

        return book.name

    class Meta:
        model = Loan
        fields = ["id",'user',"bookName", 'book',"loanDate","expireDate","returnDate"]
class UserLoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField()

    class Meta:
        model = Loan
        exclude = ['notes']


class BookLoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField()

    class Meta:
        model = Loan
        exclude = ['notes']


class BookUserLoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField()
    
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField()

    class Meta:
        model = Loan
        fields = ["id", 'user',"user_id","book_id" , 'book', "loanDate", "expireDate", "returnDate","notes"]