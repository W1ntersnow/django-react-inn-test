from .serializers import UserSerializer
from testapp.models import User
from rest_framework import generics
from django.db.models import F


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CashException(Exception):
    pass


class NotFoundException(Exception):
    pass


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        input_sum = int(self.request.data['cash'])
        inns = self.request.data['users_inn'].split(',')
        user = User.objects.filter(username=self.request.data['username'])[0]

        if user.cash >= input_sum:
            User.objects.filter(username=self.request.data['username']).update(cash=F('cash')-input_sum)
            users_by_inns = User.objects.filter(inn__in=inns)
            users_count = users_by_inns.count()
            if str(users_count).isdigit() and int(users_count) == 0:
                raise NotFoundException('users not found: ', inns)
            inc_sum = input_sum/int(users_count)
            users_by_inns.update(cash=F('cash') + inc_sum)
        else:
            raise CashException('user has only: ', user.cash)
