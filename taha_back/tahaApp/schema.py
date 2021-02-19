import graphene
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene import relay, ObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token

from tahaApp.models import *
from tahaApp.wchelper import get_products


# Make models available to graphene.Field
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = ['id']
        interfaces = (relay.Node,)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        filter_fields = ['id']
        interfaces = (relay.Node,)


class OTPNode(DjangoObjectType):
    class Meta:
        model = OTP
        filter_fields = ['id']
        interface = (relay.Node,)


class RequestOTP(graphene.Mutation):
    status = graphene.Field(String)

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.get(user=user_obj.id)
        otp = OTP(profile=profile_obj)
        otp.save()
        return RequestOTP(status="success")


class VerifyUser(graphene.Mutation):
    status = graphene.Field(String)

    class Arguments:
        username = graphene.String(required=True)
        otp_message = graphene.String(required=True)

    def mutate(self, info, username, otp_message):
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.get(user=user_obj.id)
        related_otp = OTP.objects.filter(profile=profile_obj.id)
        for otp in related_otp:
            if otp.message == otp_message and otp.valid == 'valid':
                otp.valid = 'invalid'
                profile_obj.status = 'a'
                otp.save()
                profile_obj.save()
                return VerifyUser(status="success")
        return VerifyUser(status="failed")


# CreateUser
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(ProfileNode)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
            email="",
        )
        user.set_password(password)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        # phone_number = profile_obj.phone_number
        # otp = OTP.objects.get(profile=profile_obj.id)
        # otp_send(phone_number, otp.message)
        return CreateUser(user=user, profile=profile_obj, token=token, refresh_token=refresh_token)


class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        filter_fields = ['id', 'name', 'woo_id']
        interfaces = (relay.Node,)

    def resolve_image(self, info):
        """Resolve product image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image


class ShopNode(DjangoObjectType):
    class Meta:
        model = Shop
        filter_fields = ['id', 'title', 'body']
        interfaces = (relay.Node,)


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = ['id', 'title', 'body']
        interfaces = (relay.Node,)


class RecieptNode(DjangoObjectType):
    class Meta:
        model = Receipt
        filter_fields = ['id', 'created_at']
        interfaces = (relay.Node,)


class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        filter_fields = ['id', 'created_at']
        interfaces = (relay.Node,)


class WalletNode(DjangoObjectType):
    class Meta:
        model = Wallet
        filter_fields = ['id', 'created_at']
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['id', 'username']
        interfaces = (relay.Node,)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['id', 'name']
        interfaces = (relay.Node,)


class TahaMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    verify_user = VerifyUser.Field()
    request_otp = RequestOTP.Field()


class TahaQuery(graphene.ObjectType):
    shop = relay.Node.Field(ShopNode)
    shop_list = DjangoFilterConnectionField(ShopNode)

    image = relay.Node.Field(ImageNode)
    image_list = DjangoFilterConnectionField(ImageNode)

    profile = relay.Node.Field(ProfileNode)
    profile_list = DjangoFilterConnectionField(ProfileNode)

    # otp = relay.Node.Field(OTPNode)
    # otp_list = DjangoFilterConnectionField(OTPNode)

    product = relay.Node.Field(ProductNode)
    product_list = DjangoFilterConnectionField(ProductNode)

    receipt = relay.Node.Field(RecieptNode)
    receipt_list = DjangoFilterConnectionField(RecieptNode)

    transaction = relay.Node.Field(TransactionNode)
    transaction_list = DjangoFilterConnectionField(TransactionNode)

    wallet = relay.Node.Field(WalletNode)
    wallet_list = DjangoFilterConnectionField(WalletNode)

    category = relay.Node.Field(CategoryNode)
    category_list = DjangoFilterConnectionField(CategoryNode)

    get_product = graphene.Field(ShopNode, id=graphene.String())

    def resolve_get_product(root, info, id):
        shop = Shop.objects.get(pk=id)
        return get_products(shop)
