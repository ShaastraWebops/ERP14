from users.models import ERPUser, HOSTEL_CHOICES
from django.contrib.auth.models import User
from dept.models import Dept, Subdept


# _____________--- MAKE USERS ---______________#
def populate_db():
    # MAKE DEPARTMENTS
    for i in range(3):
        if Dept.objects.filter(name="Dept" + str(i)).count():
            continue
        d = Dept()
        d.name = "Dept" + str(i)
        d.save()
    
    # MAKE SUB DEPTS
    for d in Dept.objects.filter(name=):
        for i in range(2):
            if Subdept.objects.filter(name="Subdept" + str(i) + " for " + d.name).count():
                continue
            sd = Subdept()
            sd.name = "Subdept" + str(i) + " for " + d.name
            sd.dept = d
            sd.save()
    
    # MAKE CORES
    for i in range(1):
        if ERPUser.objects.filter(nickname="Corenick" + str(i)).count():
            continue
        u = ERPUser()
        if User.objects.filter(username = '_core'+str(i)).count(): # user doesnt exist
            u.user = User.objects.get(username = '_core'+str(i))
        else:
            u.user = User.objects.create_user(
                username = '_core'+str(i), 
                password = str(i)
            )
        u.user.username = '_core'+str(i)
        u.user.password = str(i)
        u.user.email = "core" + str(i) + "email@shaastra.org",  
        u.user.first_name = "Core" + str(i)
        u.user.last_name = "ACore"
        if Dept.objects.get(name="Dept"+str(i)):
            u.dept = Dept.objects.get(name="Dept"+str(i))
        elif Dept.objects.get(name="Dept0"):
            u.dept = Dept.objects.get(name="Dept0")
        else:
            print "Error, there is no dept to assing the user to"
            return
        if Dept.objects.filter(name="Subdept" + str(i) + " for Dept" + str(i)).count():
            u.dept = Dept.objects.get(name="Subdept" + str(i) + " for Dept" + str(i))
        elif Dept.objects.filter(name="Subdept0 for Dept0").count():
            u.dept = Dept.objects.get(name="Subdept0 for Dept0")
        else:
            print "Error, there is no SUBdept to assing the user to"
            return
        u.status = 2
        u.core_relations = u.dept
        u.nickname = "Corenick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOTEL_CHOICES)][0]
        u.room_no = i%1000
        u.save()
    
    # MAKE COORDS
    for i in range(5):
        if ERPUser.objects.filter(nickname="Coordnick" + str(i)).count():
            continue
        u = ERPUser()
        u.user = User.objects.create_user(
            username = '_coord'+str(i), 
            email = "coord" + str(i) + "email@shaastra.org",  
            password = str(i)
        )
        u.user.first_name = "Coord" + str(i)
        u.user.last_name = "ACoord"
        if Dept.objects.get(name="Dept"+str(i)):
            u.dept = Dept.objects.get(name="Dept"+str(i))
        elif Dept.objects.get(name="Dept0"):
            u.dept = Dept.objects.get(name="Dept0")
        else:
            print "Error, there is no dept to assing the user to"
            return
        if Dept.objects.filter(name="Subdept" + str(i) + " for Dept" + str(i)).count():
            u.dept = Dept.objects.get(name="Subdept" + str(i) + " for Dept" + str(i))
        elif Dept.objects.filter(name="Subdept0 for Dept0").count():
            u.dept = Dept.objects.get(name="Subdept0 for Dept0")
        else:
            print "Error, there is no SUBdept to assing the user to"
            return
        u.status = 0
        u.core_relations = u.dept
        u.nickname = "Coordnick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOTEL_CHOICES)][0]
        u.room_no = i%1000
        u.save()
    
    # MAKE SUPERCOORDS
    for i in range(1):
        if ERPUser.objects.filter(nickname="Supernick" + str(i)).count():
            continue
        u = ERPUser()
        u.user = User.objects.create_user(
            username = '_super'+str(i), 
            email = "super" + str(i) + "email@shaastra.org",  
            password = str(i)
        )
        u.user.first_name = "Super" + str(i)
        u.user.last_name = "ASuper"
        if Dept.objects.get(name="Dept"+str(i)):
            u.dept = Dept.objects.get(name="Dept"+str(i))
        elif Dept.objects.get(name="Dept0"):
            u.dept = Dept.objects.get(name="Dept0")
        else:
            print "Error, there is no dept to assing the user to"
            return
        if Dept.objects.filter(name="Subdept" + str(i) + " for Dept" + str(i)).count():
            u.dept = Dept.objects.get(name="Subdept" + str(i) + " for Dept" + str(i))
        elif Dept.objects.filter(name="Subdept0 for Dept0").count():
            u.dept = Dept.objects.get(name="Subdept0 for Dept0")
        else:
            print "Error, there is no SUBdept to assing the user to"
            return
        u.status = 1
        u.core_relations = u.dept
        u.nickname = "Supernick" + str(i)
        u.chennai_number = str(i%10)*10
        u.summer_number = str((i%100)/10)*10
        u.summer_stay = "full"
        u.hostel = HOSTEL_CHOICES[i%len(HOTEL_CHOICES)][0]
        u.room_no = i%1000
        u.save()
    
    # MAKE INTRA DEPARTMENTAL TASKS - ACCEPTED
    
    
    # MAKE INTRA DEPARTMENTAL TASKS - NEARLY COMPLETE
    
    # MAKE INTRA DEPARTMENTAL TASKS - REPORTED COMPLETE
    
    # MAKE INTRA DEPARTMENTAL TASKS - COMPLETED
    
    # MAKE CROSS DEPARTMENTAL TASKS - UNACCEPTED
    
    # MAKE CROSS DEPARTMENTAL TASKS - ACCEPTED
    
