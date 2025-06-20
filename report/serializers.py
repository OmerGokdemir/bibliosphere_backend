from rest_framework import serializers
from book.models import Book
from loans.models import Loan
from user.models import User


class ReportSerializer(serializers.Serializer):
    books = serializers.IntegerField()
    authors = serializers.IntegerField()
    publishers = serializers.IntegerField()
    categories = serializers.IntegerField()
    loans = serializers.IntegerField()
    unReturnedBooks = serializers.IntegerField()
    expiredBooks = serializers.IntegerField()
    members = serializers.IntegerField()


class NewBookSerializer(serializers.ModelSerializer):
    total_loans = serializers.IntegerField(read_only=True)
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        loans = Loan.objects.filter(book=obj.id)
        amount = 0
        for i in loans:
            amount += 1
        return amount

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'isbn', 'pageCount', 'publishDate', 'image',
            'loanable', 'shelfCode', 'active', 'featured', 'createDate',
            'builtIn', 'authorId', 'publisherId',"amount", 'categoryId', 'total_loans'
        )

class ReportBookSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True)
    authorName = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    publisherName = serializers.SerializerMethodField()
    userName = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    loanDate = serializers.SerializerMethodField()
    expireDate =serializers.SerializerMethodField()


    def get_userName(self, obj):
        loans = Loan.objects.filter(book=obj.id)
        if loans.exists():
            user = loans.first().user
            return f"{user.firstName} {user.lastName}" if user else ""
        return ""

    def get_expireDate(self,obj):
        loans = Loan.objects.filter(book=obj.id)
        if loans.exists():
            date = str(loans.first().expireDate)
            date = date[0:10]
            return date
        return ""

    def get_loanDate(self,obj):
        loans = Loan.objects.filter(book=obj.id)
        if loans.exists():
            date = str(loans.first().loanDate)
            date = date[0:10]
            return date
        return ""



    def get_userId(self, obj):
        loans = Loan.objects.filter(book=obj.id)
        if loans.exists():
            user = loans.first().user
            return user.id if user else None
        return None

    def get_authorName(self, obj):
        author_names = [author.name for author in obj.authorId.all()]
        return ", ".join(author_names) if author_names else ""

    def get_categoryName(self, obj):
        category_names = [category.name for category in obj.categoryId.all()]
        return ", ".join(category_names) if category_names else ""

    def get_publisherName(self, obj):
        return obj.publisherId.name

    class Meta:
        model = Book
        fields = ["id","userName","loanDate","userId", "name", "authorName", "categoryName", "publisherName", "image", "pageCount", "isbn", "authorId",
                  "publisherId", "categoryId", "publishDate", "loanable", "shelfCode", "active", "featured",
                  "createDate", "builtIn",  "expireDate"]

class NewUserSerializer(serializers.ModelSerializer):
    total_loans = serializers.IntegerField(read_only=True)
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        loans = Loan.objects.filter(user=obj.id)
        amount = 0
        for i in loans:
            amount += 1
        return amount

    class Meta:
        model = User
        fields = ('id','firstName','lastName',"score",'address','phone','birthDate','email','password',"is_superuser","is_staff", "amount",'total_loans')