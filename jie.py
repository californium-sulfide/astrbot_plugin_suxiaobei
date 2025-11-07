import random
from .dataIO import save, load
path='./data/order_jie'
main_course_name=['炒饼','炒面','炒河粉','炒饭','炒米线','炒方便面']
main_course_price=[12,12,12,12,12,12]
main_course_weight=[100.0,50.0,10.0,100.0,10.0,10.0]
bind_course_name=['蔬菜']
bind_course_price=[2]

sausage_name=['王中王','藤椒肠','大肉肠','鸡肉肠']
sausage_price=[2,3,4,2]
sausage_probability=[0.5,0.2,0.1,0.3]

addition_name=['鸡蛋','鸡肉','猪肉','鱼豆腐','大海带丝',
                '梅菜笋丝','爽口萝卜','爽口黄瓜','金针菇','红油豆角','爽口菜','雪里红','小海带丝','竹笋',
                '小卫龙','小土豆丝','小开胃丝','小葱排骨粒',
                '大卫龙','大开胃丝','大土豆丝','大长辣条']
addition_price=[2,4,5,2,2,
                2,2,2,2,3,3,3,1,2,
                1,1,1,1,
                4,4,3,3]
addition_probability=[0.05,0.02,0.1,0.2,0.02,
                        0.02,0.05,0.02,0.02,0.02,0.02,0.02,0.02,0.02,
                        0.4,0.1,0.2,0.02,
                        0.1,0.05,0.02,0.02]
zh_num=['零','一','两','三','四','五','六','七','八','九','十','十一','十二','十三','十四','十五','十六','十七','十八','十九','二十']
def random_jie():
    text="点一份"
    price=0
    index=0
    r=random.random()*sum(main_course_weight)
    while r>main_course_weight[index]:
        r-=main_course_weight[index]
        index+=1
    main_course_list=[index]
    price+=main_course_price[index]
    bind_course_list=[]
    for index in range(0,len(bind_course_name)):
        if random.random()<0.1:
            text+='，不加'+bind_course_name[index]
            price-=bind_course_price[index]
        else:
            num=1
            while random.random()<0.2:
                num+=1
                price+=bind_course_price[index]
            bind_course_list.append(num)
    sausage_list=[0,]
    remove_bind=False
    while random.random()<0.3:
        index=random.randint(0,len(sausage_name)-1)
        sausage_list.append(index)
        price+=sausage_price[index]
    if random.random()<0.5 and len(sausage_list)>1:
        sausage_list.remove(0)
        price-=2
    if sausage_list.count(0)==0:
        remove_bind=True
    if len(sausage_list)==0:
        text+='，不加肠'
    elif len(sausage_list)==1:
        if remove_bind:
            text+='，换'+sausage_name[sausage_list[0]]
    else:
        if remove_bind:
            text+='，换'
        else:
            text+='，加'
            sausage_list.remove(0)
        duplicated_sausage=False
        for index in range(0,len(sausage_name)):
            if sausage_list.count(index)>1:
                duplicated_sausage=True
                break
        sausage_set=set(sausage_list)
        pos=len(sausage_set)
        for index in sausage_set:
            if sausage_list.count(index)==0:
                pass
            elif sausage_list.count(index)==1:
                if not duplicated_sausage:
                    text+=sausage_name[index]
                else:
                    text+=str(zh_num[1])+'根'+sausage_name[index]
            elif sausage_list.count(index)>1:
                text+=str(zh_num[sausage_list.count(index)])+'根'+sausage_name[index]
            if pos==1:
                pass
            elif pos==2:
                text+='和'
            else:
                text+='、'
            pos-=1
    for index in range(0,len(addition_name)):
        num=0
        while random.random()<addition_probability[index]:
            num+=1
            price+=addition_price[index]
        if num==0:
            pass
        elif num==1:
            text+='，加'+addition_name[index]
        else:
            text+='，加'+str(zh_num[num])+'份'+addition_name[index]
    text+='。一共'+str(price)+'元。'
    return text
    return {'jie_list':[main_course_list,sausage_list],'price':price}
def dump_jie(jie_list:list[list[int]],price:int):
    text='点一份'
    [main_course_list,bind_course_list,sausage_list,addition_list]=jie_list
    main_course=main_course_list[0]
    text+=main_course_name[main_course]
    for index in range(0,len(bind_course_name)):
        if bind_course_list[index]==0:
            text+='，不加'+bind_course_name[index]
        elif bind_course_list[index]==1:
            pass
        elif bind_course_list[index]==2:
            text+='，加'+bind_course_name[index]
        else:
            text+='，加'+str(zh_num[bind_course_list[index]-1])+'份'+bind_course_name[index]
    remove_bind=True if sausage_list.count(0)==0 else False

    return text
    pass
def dump_random_jie():
    pass
    #return dump_jie(**random_jie())
def parse_jie(text:str):
    return