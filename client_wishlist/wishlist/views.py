from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from customers.auth import authenticate
from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer
from wishlist.wishlist_svc import get_or_update, delete_product_from_whishlist


class WishListDetailView(APIView):
    def get(self, request, customer_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                wishlist = get_object_or_404(Wishlist, customer__id=customer_id)
                serializer = WishlistSerializer(wishlist)
                response = Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)
        return response

    def post(self, request, customer_id):
        wishlist_data = request.data
        wishlist_data["customer"] = customer_id

        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                serializer = WishlistSerializer(data=wishlist_data)
                if serializer.is_valid():
                    serializer.save()
                    response = Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)

        return response

    def delete(self, request, customer_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                wishlist = get_object_or_404(Wishlist, customer__id=customer_id)
                wishlist.delete()
                response = Response(status=status.HTTP_204_NO_CONTENT)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)
        return response


class WislistUpdateView(APIView):
    def post(self, request, customer_id, product_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                wishlist = get_or_update(customer_id, product_id)
                serializer = WishlistSerializer(wishlist)
                response = Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)

        return response

    def delete(self, request, customer_id, product_id):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            authenticated = authenticate(customer_id=customer_id, token=token)
        except KeyError:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if authenticated:
                whishlist = delete_product_from_whishlist(customer_id, product_id)
                serializer = WishlistSerializer(whishlist)
                response = Response(serializer.data, status=status.HTTP_200_OK)
            else:
                response = Response(status=status.HTTP_401_UNAUTHORIZED)

        return response
