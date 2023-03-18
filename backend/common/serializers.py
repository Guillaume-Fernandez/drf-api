from rest_framework import serializers

class CommonHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    def use_pk_only_optimization(self):
        """
        Disable a rest_framework optimization to do a pretty print in admin interface.
        ForeignKey can be represented by their __str__ instead of just id.
        API/Json format will only print url.
        May impact performances and is useless in format != admin
        """
        return False
