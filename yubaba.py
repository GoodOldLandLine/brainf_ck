#!/usr/bin/env python
# coding: utf-8

# In[3]:


from exec_func import execute, set_max_loops, optimizer
from code_generator import Var
set_max_loops(100000000)

p = Var()
loop = Var()
flag = Var()
i = Var()
char = Var()
eof = Var()
temp = Var()
seed = Var()
c0 = Var()
c1 = Var()
c2 = Var()
c3 = Var()
c4 = Var()
c5 = Var()
c6 = Var()
c7 = Var()
c8 = Var()
c9 = Var()
c10 = Var()
c11 = Var()
new_name0 = Var()
new_name1 = Var()
new_name2 = Var()


code = (
    ""
    +seed.getchar()
    
    +p.printstr("契約書だよ。そこに名前を書きな。\n")
    
    +flag.copy(12)
    +loop.while_v(
        flag,
        ""
        +char.getchar()
        
        +temp.copy(i)
        +temp.eq(0)
        +temp.if_true(c0.copy(char),"")
        +temp.copy(i)
        +temp.eq(1)
        +temp.if_true(c1.copy(char),"")
        +temp.copy(i)
        +temp.eq(2)
        +temp.if_true(c2.copy(char),"")
        +temp.copy(i)
        +temp.eq(3)
        +temp.if_true(c3.copy(char),"")
        +temp.copy(i)
        +temp.eq(4)
        +temp.if_true(c4.copy(char),"")
        +temp.copy(i)
        +temp.eq(5)
        +temp.if_true(c5.copy(char),"")
        +temp.copy(i)
        +temp.eq(6)
        +temp.if_true(c6.copy(char),"")
        +temp.copy(i)
        +temp.eq(7)
        +temp.if_true(c7.copy(char),"")
        +temp.copy(i)
        +temp.eq(8)
        +temp.if_true(c8.copy(char),"")
        +temp.copy(i)
        +temp.eq(9)
        +temp.if_true(c9.copy(char),"")
        +temp.copy(i)
        +temp.eq(10)
        +temp.if_true(c10.copy(char),"")
        +temp.copy(i)
        +temp.eq(11)
        +temp.if_true(c11.copy(char),"")
        
        +i.add(1)
        +temp.copy(i)
        +temp.eq(flag)
        +temp.if_true(flag.copy(0), ""))
    
    +temp.printstr("ふん。")
    +c0.show()
    +c1.show()
    +c2.show()
    +c3.show()
    +c4.show()
    +c5.show()
    +c6.show()
    +c7.show()
    +c8.show()
    +c9.show()
    +c10.show()
    +c11.show()
    +temp.printstr("というのかい。贅沢な名だねぇ。\n")
    
    
    
    +temp.copy(0)
    +temp.eq(seed)
    +temp.if_true(new_name0.copy(c0)
                 +new_name1.copy(c1)
                 +new_name2.copy(c2),"")
    +temp.copy(1)
    +temp.eq(seed)
    +temp.if_true(new_name0.copy(c3)
                 +new_name1.copy(c4)
                 +new_name2.copy(c5),"")
    +temp.copy(2)
    +temp.eq(seed)
    +temp.if_true(new_name0.copy(c6)
                 +new_name1.copy(c7)
                 +new_name2.copy(c8),"")
    +temp.copy(3)
    +temp.eq(seed)
    +temp.if_true(new_name0.copy(c9)
                 +new_name1.copy(c10)
                 +new_name2.copy(c11),"")
    
    +temp.printstr("今からお前の名前は")
    +new_name0.show()+new_name1.show()+new_name2.show()
    +temp.printstr("だ。いいかい、")
    +new_name0.show()+new_name1.show()+new_name2.show()
    +temp.printstr("だよ。分かったら返事をするんだ、")
    +new_name0.show()+new_name1.show()+new_name2.show()
    +temp.printstr("!!\n")
)
print(optimizer(code))


# In[6]:


input_code="\x02山田太郎"
execute(optimizer(code), input_code=input_code, prohibited_overflow=True)


# In[ ]:




