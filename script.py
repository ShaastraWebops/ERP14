from barcode.views import *
def fn(shid):
    try:
        p = UserProfile.objects.using('mainsite').filter(shaastra_id = 'SHA14'+shid)[0]
        if not is_junk(p.shaastra_id):
            return '#'
    except:
        return '#'
    return p
print '!!!!!!!!'
junklist = [up for up in UserProfile.objects.using('mainsite').all() if is_junk(up.shaastra_id)]
numlist = [up for up in UserProfile.objects.using('mainsite').all() if up.shaastra_id.isdigit()]
corrlist = [ (n,fn(n.shaastra_id)) for n in numlist if fn(n.shaastra_id)!='#']
#corrlist = [(j,fn(j)) for j in junklist if j.shaastra_id[3:].isdigit() and fn(j)!='#']
#jlist = [c[1] for c in corrlist if is_junk(c[1].shaastra_id)]
#clist = [c for c in corrlist if is_junk(c[1].shaastra_id)]
for c in corrlist:
    c[1].college = c[0].college
    c[1].save()
    c[1].mobile_number = c[0].mobile_number
    c[1].age = c[0].age
    c[1].gender = c[0].gender
    c[1].branch = c[0].branch
    c[1].save()
    c[1].user.first_name = c[0].user.first_name
    c[1].user.last_name = c[0].user.last_name
    #c[1].user.username = c[0].user.username + " "
    c[1].user.is_staff = False
    c[1].user.save()
    print '!'
    c[1].save()
junklist2 = [up for up in UserProfile.objects.using('mainsite').all() if is_junk(up.shaastra_id)]

