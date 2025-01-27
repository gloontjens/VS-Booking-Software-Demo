from .models import MusicList


# def refresh_musiclist():
#     listobject = MusicList.objects.get(pk=1)
#     currentmusiclist = listobject.list.splitlines()
#     return currentmusiclist


listobject = MusicList.objects.get(pk=1)
currentmusiclist = listobject.list.splitlines()
