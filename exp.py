import mysql.connector as c
from datetime import datetime
con=c.connect(host="localhost", user="root", passwd="Yu9899726634@", database="dbms_final")
if(con.is_connected):
    print("connected")

user_id=input("Enter user_id :  ")
print("S.no       Feature")
print(" 1. See chats with user with user_id a")
print(" 2. Message user with user_id a")
print(" 3. See status of user a if any")
print(" 4. See Group message ")
print(" 5. see admins of the group")
print(" 6. See all starred messages of user with other user b")
print(" 7. Fetch all the groups user a is part of")
print(" 8. All starred messages in group a")
print(" 9. Get group description")
print(" 10. Get all details of a user")
print(" 11. add status")
print(" 12. Send message to a group")
print(" 13. delete personal message ")
print(" 14. delete message from a group")
print(" 15. Mark a message starred")
print(" 16. Mark a message starred in grp")
print(" 17. Remove message from starred in personal chat")
print(" 18. Remove message from starred in grp")
print(" 19. Logout")


 
while(True):
    num=input("enter s.no of feature u want to perform : ")
    if(num==1):
        choice = input("how would you like to search the other user(0--> id or 1 --> name): ")
        if(choice == 0):
            user2=input("Enter id of user you want to see chats with : ")
        elif(choice == 1):
            user_name = raw_input("Enter the name of the user: ")
            cursor = con.cursor()
            query = ("select u.user_id, u.first_name, u.last_name from dbms_final.user u where u.first_name LIKE " + "'%"+user_name+"%'"+" or u.last_name LIKE "+ "'%"+user_name+"%'")
            cursor.execute(query)
            data=cursor.fetchall()


            cursor1=con.cursor()
            query1=("select p.chat_from from dbms_final.personal_message p where p.chat_to = "+ str(user_id))
            cursor1.execute(query1)
            data1=cursor1.fetchall()
            list_a = data1[0]

            cursor2=con.cursor()
            query2=("select p.chat_to from dbms_final.personal_message p where p.chat_from = "+ str(user_id))
            cursor2.execute(query2)
            data2=cursor2.fetchall()
            list_a.append(data2[0])

            for(a,b,c) in data:
                if(a in list_a):
                    print("Name --> " + b+" "+c)
                    print("User_id --> "+str(a))
                    print("\n")
            # print(data)
            user2 = input("Enter id of user you want to see chats with : ")
        cursor1=con.cursor()
        query=("select p.chat_desc, p.time_stamp, p.chat_from from dbms_final.personal_message p where p.chat_from = "+ str(user_id) +  " and p.chat_to = " + str(user2)+ 
        " or p.chat_from= "+ str(user2) +" and p.chat_to= "+ str(user_id))
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c) in data:
            print(c)
            print(a+"    "+b+"\n")

    if(num==2):
        cursor=con.cursor()
        query=("select p.chat_id, user1_id, user2_id from personal_chat p where user1_id= "+str(user_id) +" or user2_id= "+str(user_id))
        
        
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b,c) in data:
            print(str(a))
            print("user_id of 1 --> "+str(b))
            print("user_id of 2 --> "+str(c))
        user2=input("Enter id of user you want to message to : ")
        cursor1=con.cursor()
        query1=("select p.chat_id from personal_chat p where p.user1_id = " + str(user2) +" and p.user2_id = " +  str(user_id)+" or p.user1_id = "+str(user_id)+" and p.user2_id= "+str(user2))
        cursor1.execute(query1)
        data=cursor1.fetchone()
        chatid=data[0]

        cursor2=con.cursor()
        query2=("SELECT COUNT(*) as count_status FROM personal_message")
        cursor2.execute(query2)
        data=cursor2.fetchall()
        no=data[0][0]+1

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        starred=0
        status=0
        cursor3=con.cursor()

        desc=raw_input("Enter message you want to send")
        query3=("INSERT INTO personal_message(msg_id, chat_id, chat_desc, time_stamp,chat_from,chat_to,starred,status_msg)"
               "VALUES (%s, %s, %s, %s,%s,%s,%s,%s)")
        val=(no, chatid, desc,current_time,user_id,user2,starred,status)
        cursor3.execute(query3,val)
        con.commit()
        print("message sent")

        # query1=("insert into personal_message(msg_id,chat_id,chat_desc,time_stamp,chat_from,chat_to,starred,status_msg)".values())
        

    if(num==3):
        user2=input("Enter id of user you want to see status of : ")
        cursor=con.cursor()
        query=("select s.status_data, s.time_stamp from dbms_final.user_status s where s.user_id = "+ str(user2))
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b) in data:
            print(b)
            print(a)
            print("")
    if(num==4):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "    grp id -->  " + str(b))
        group=input("Enter id of grp you want to see message of : ")
        cursor1=con.cursor()
        query1=("select g.msg_desc, g.from_id, g.time_stamp from grp_message g where g.grp_id= "+ str(group)+" ORDER BY g.time_stamp desc")
        cursor1.execute(query1)
        data=cursor1.fetchall()
        for(a,b,c) in data:
            print(b)
            print(a+"   "+c)
    if(num==5):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        print("S.no      group name      group id")
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "       " + str(b))
        group=input("Enter id of grp you want to see admins of : ")
        cursor1=con.cursor()
        query1=("select u.first_name, u.last_name, g.name as grp_name from dbms_final.grp_admin ga , dbms_final.grp g, dbms_final.user u where ga.grp_id =" +str(group)+" and ga.grp_id = g.grp_id and ga.from_id = u.user_id")
        cursor1.execute(query1)
        data=cursor1.fetchall()
        print("admins of group with group id "+str(group))
        index=0
        for(a,b,c) in data:
            print("S.no   "+ str(index)+"   grp id -->  "+ a + " "+b)

    if(num==6):
        user2=input("Enter id of user you want to see starred messages with : ")
        cursor=con.cursor()
        query=("select p.chat_desc, p.time_stamp, p.chat_from from dbms_final.personal_message p where p.chat_from = "+ str(user_id) +  " and p.chat_to = " + str(user2)+" and p.starred=1"+ 
        " or p.chat_from= "+ str(user2) +" and p.chat_to= "+ str(user_id)+" and p.starred=1")
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b,c) in data:
            print(c)
            print(a+"    "+b+"\n")
        
    if(num==7):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + " " + str(b))

    if(num==8):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "  grp id --> " + str(b))
        group=input("Enter id of grp you want to see starred message of : ")
        cursor1=con.cursor()
        query1=("select g.msg_desc, g.from_id, g.time_stamp from grp_message g where g.grp_id= "+ str(group)+" and g.starred=1  ORDER BY g.time_stamp desc")
        cursor1.execute(query1)
        data=cursor1.fetchall()
        for(a,b,c) in data:
            for(a,b,c) in data:
                print(b)
                print(a+"   "+c)
                print()
    if(num==9):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "   grp id --> " + str(b))
        group=input("Enter id of grp you want to see message of : ")
        cursor1=con.cursor()
        query1="select g.name, g.about from dbms_final.grp g where g.grp_id = "+ str(group)
        cursor1.execute(query1)
        data=cursor1.fetchall()
        print("group id -->  "+ str(group))
        print("group name --> "+data[0][0])
        print("goup description --> "+data[0][1])
        print("")

    if(num==10):
        user2=input("enter user id of user you want to get details :  ")
        cursor=con.cursor()
        query=("select * from dbms_final.user u where u.user_id = "+ str(user2))
        cursor.execute(query)
        data=cursor.fetchall()
        print("user id --> "+ str(user2))
        print("user name --> "+ data[0][1] +" " + data[0][2])
        print("email id  --> "+ data[0][3])
        print("mobile no -->"+ data[0][4])
        print("about -->    "+ data[0][5])
    if(num==11):
        cursor=con.cursor()
        query=("SELECT COUNT(*) as count_status FROM user_status")
        cursor.execute(query)
        data=cursor.fetchall()

        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # status_desc=input("Enter status data : ")
        status_desc=raw_input("Enter status data")
        status_no=data[0][0]+1
        cursor1=con.cursor()
        print(data)
        query3=("INSERT INTO user_status(status_id, user_id, time_stamp, status_data)"
               "VALUES (%s, %s, %s, %s)")
        val=(status_no, user_id, current_time, status_desc)
        cursor1.execute(query3,val)
        con.commit()
        # data=cursor1.fetchall()
        print("data inserted successfully")
    if(num==12):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "   grp id --> " + str(b))

        group=input("Enter id of grp you want to see message of : ")

        now = datetime.now()
        current_time = now.strftime("%H:%M")

        cursor2=con.cursor()
        query2=("SELECT COUNT(*) as count_status FROM grp_message")
        cursor2.execute(query2)
        data=cursor2.fetchall()
        no=data[0][0]+1

        desc=raw_input("Enter message you want to send")

        starred=0
        cursor3=con.cursor()
        query3=("INSERT INTO grp_message(msg_id, grp_id,from_id, msg_desc, time_stamp,starred)"
               "VALUES (%s, %s, %s, %s,%s,%s)")
        val=(no, group,user_id, desc,current_time,starred)
        cursor3.execute(query3,val)
        con.commit()
        print("message sent")
    if(num==13):
        cursor=con.cursor()
        query=("select p.chat_id, user1_id, user2_id from personal_chat p where user1_id= "+str(user_id) +" or user2_id= "+str(user_id))
        
        
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b,c) in data:
            print(str(a))
            print("user_id of 1 --> "+str(b))
            print("user_id of 2 --> "+str(c))
        user2=input("Enter id of user you want to delete message of : ")

        cursor1=con.cursor()
        query=("select p.chat_desc, p.time_stamp, p.chat_from,p.msg_id from dbms_final.personal_message p where p.chat_from = "+ str(user_id) +  " and p.chat_to = " + str(user2)+ 
        " or p.chat_from= "+ str(user2) +" and p.chat_to= "+ str(user_id))
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> " +str(d)+" user_id --> "+str(c))
            print(a+"    "+b+"\n")
        m_id=input("Enter message id you want to delete : ")
        if(len(data)!=0):
            cursor1=con.cursor()
            query=("delete from personal_message where msg_id= "+str(m_id))
            cursor1.execute(query)
            con.commit()
            print("deletion successful")
    
    if(num==14):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        print("S.no      group name      group id")
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "       " + str(b))
        group=input("Enter id of grp you want to delete message of of : ")
        cursor1=con.cursor()
        query="select g.msg_id, g.msg_desc, g.time_stamp,g.from_id from dbms_final.grp_message g where g.from_id= "+str(user_id)+ " and g.grp_id= "+str(group)
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> "+str(a)+"  user_id --> "+str(d))
            print(b+ "      "+c)
        if(len(data)!=0):
            m_id=input("Enter message id you want to delete : ")
            cursor2=con.cursor()
            query=("delete from grp_message where msg_id= "+str(m_id))
            cursor2.execute(query)
            con.commit()
            print("deletion successful")
    if(num==15):
        cursor=con.cursor()
        query=("select p.chat_id, user1_id, user2_id from personal_chat p where user1_id= "+str(user_id) +" or user2_id= "+str(user_id))
        
        
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b,c) in data:
            print(str(a))
            print("user_id of 1 --> "+str(b))
            print("user_id of 2 --> "+str(c))
        user2=input("Enter id of user you want to mark a message starred : ")

        cursor1=con.cursor()
        query=("select p.chat_desc, p.time_stamp, p.chat_from,p.msg_id from dbms_final.personal_message p where p.chat_from = "+ str(user_id) +  " and p.chat_to = " + str(user2)+ 
        " or p.chat_from= "+ str(user2) +" and p.chat_to= "+ str(user_id))
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> " +str(d)+" user_id --> "+str(c))
            print(a+"    "+b+"\n")
        m_id=input("Enter message id you want to mark starred : ")
        if(len(data)!=0):
            cursor1=con.cursor()
            query=("update personal_message set starred=1 where msg_id= "+str(m_id))
            cursor1.execute(query)
            con.commit()
            print("marked starred successfully successful")
    if(num==16):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        print("S.no      group name      group id")
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "       " + str(b))
        group=input("Enter id of grp you want to mark message starred : ")
        cursor1=con.cursor()
        query="select g.msg_id, g.msg_desc, g.time_stamp,g.from_id from dbms_final.grp_message g where g.from_id= "+str(user_id)+ " and g.grp_id= "+str(group)
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> "+str(a)+"  user_id --> "+str(d))
            print(b+ "      "+c)
        if(len(data)!=0):
            m_id=input("Enter message id you want to mark starred : ")
            cursor2=con.cursor()
            query=("update grp_message set starred=1 where msg_id= "+str(m_id))
            cursor2.execute(query)
            con.commit()
            print("message marked starred ")
    if(num==17):
        cursor=con.cursor()
        query=("select p.chat_id, user1_id, user2_id from personal_chat p where user1_id= "+str(user_id) +" or user2_id= "+str(user_id))
        
        
        cursor.execute(query)
        data=cursor.fetchall()
        for(a,b,c) in data:
            print(str(a))
            print("user_id of 1 --> "+str(b))
            print("user_id of 2 --> "+str(c))
        user2=input("Enter id of user you want to remove message from starred : ")

        cursor1=con.cursor()
        query=("select p.chat_desc, p.time_stamp, p.chat_from,p.msg_id from dbms_final.personal_message p where p.chat_from = "+ str(user_id) +  " and p.chat_to = " + str(user2)+ 
        " or p.chat_from= "+ str(user2) +" and p.chat_to= "+ str(user_id))
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> " +str(d)+" user_id --> "+str(c))
            print(a+"    "+b+"\n")
        m_id=input("Enter message id you want to remove from starred : ")
        if(len(data)!=0):
            cursor1=con.cursor()
            query=("update personal_message set starred=0 where msg_id= "+str(m_id))
            cursor1.execute(query)
            con.commit()
            print("message removed from starred successfully")
    if(num==18):
        cursor=con.cursor()
        query=("select g.name, g.grp_id from dbms_final.group_user gu, dbms_final.grp g where gu.user_id = "+str(user_id) +" and gu.grp_id = g.grp_id")
        cursor.execute(query)
        data=cursor.fetchall()
        index=0
        print("S.no      group name      group id")
        for(a,b) in data:
            index=index+1
            print(str(index)+"  " + a + "       " + str(b))
        group=input("Enter id of grp you want to remove message from starred : ")
        cursor1=con.cursor()
        query="select g.msg_id, g.msg_desc, g.time_stamp,g.from_id from dbms_final.grp_message g where g.from_id= "+str(user_id)+ " and g.grp_id= "+str(group)
        cursor1.execute(query)
        data=cursor1.fetchall()
        for(a,b,c,d) in data:
            print("msg_id --> "+str(a)+"  user_id --> "+str(d))
            print(b+ "      "+c)
        if(len(data)!=0):
            m_id=input("Enter message id you want to remove from starred : ")
            cursor2=con.cursor()
            query=("update grp_message set starred=0 where msg_id= "+str(m_id))
            cursor2.execute(query)
            con.commit()
            print("message mremove from starred successfully")
    if(num==19):
        print("you are logged out")
        break