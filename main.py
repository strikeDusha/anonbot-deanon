from aiogram import Bot,Dispatcher,executor,types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage 

import time

from cfg import *
from db import *

#FSM scripting
storage=MemoryStorage
class fsm(StatesGroup):
    getmsg = State()

#bot initt
bot = Bot(debug,parse_mode='MarkDownV2')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"],state=None)
async def init(message:types.Message,state:FSMContext):
    
    global ref
    ref = message.get_args()
    
    for i in adminids:
        await bot.send_message(i,f"`new bot user\n{message.from_user.id} \n{message.from_user.full_name}` \n@{message.from_user.username}\nот юзера {ref}")
    
   
    
    #start logic 
    if(insert_account(message.from_user.id,message.from_user.full_name,message.from_user.username,ref)):
        for i in adminids:
            await bot.send_message(i,f"`new bot user\n{message.from_user.id} \n{message.from_user.full_name}` \n@{message.from_user.username}\nот юзера {ref}")
        if ref:
            await bot.send_message(message.from_user.id,'*Напишите что вы хотели сказать?*')
            await fsm.getmsg.set()
            await state.update_data(chat_id=ref)
        else:    
            await message.answer(f"*Привет {message.from_user.full_name}!* Тут ты можешь отправлять или принимать анонимные сообщения! \n\n`{href}{message.from_user.id}` \n\n*Скопируй эту ссылку, люди смогут написать тебе,перейдя по ней*")
    else:    
        await message.answer(f"*Привет {message.from_user.full_name}!* Тут ты можешь отправлять или принимать анонимные сообщения! \n\n`{href}{message.from_user.id}` \n\n*Скопируй эту ссылку, люди смогут написать тебе,перейдя по ней*")


#main logic     
@dp.message_handler(state=fsm.getmsg)
async def get_messagegetmsg(message:types.Message, state: FSMContext):

    
    async with state.proxy() as d:
        d = message.text
    #error type message = /start 123123123 handler
    #if it will handle it bot will fix in this statement
    if d[:6] =="/start":
        refer=d[7:]
        
        await bot.send_message(adminids[0],f"`id next refer {refer}\nid old refer {ref}\nid eblan {message.from_user.id} `")
        await message.answer(f'`Введите сообщение сначала предыдущему человеку, а потом перейдя по ссылке ответьте следующему`')
        await state.first()
    else:
        #replying messages to admins
        await message.answer(f"*Ваше сообщение успешно отправлено!*\nТекст\n*{d}*")
        await bot.send_message(ref, f'Тебе пришло новое сообщение!\n\n*{d}*')
        await bot.send_message(adminids[0], f'`new message\n\nkomu {ref}\n{d}\not kogo {message.from_user.full_name} `\n@{message.from_user.username}')
        await bot.send_message(adminids[1], f'`new message\n\nkomu {ref}\n{d}\not kogo {message.from_user.full_name}` \n@{message.from_user.username}')
        await state.reset_state(with_data=True)

 
 
 
#handling messages without logic
@dp.message_handler()
async def idk(message:types.Message):
    await message.answer("я тебя не понимаю\n*ВВЕДИ КОМАНДУ /start ДЛЯ ВОЗВРАЩЕНИЯ В МЕНЮ*")

# @dp.message_handler(commands=["/getgb"],)
# async def idk(message:types.Message):
#my try to make db to this bot,but i am too lazy to do this

 
#webhooks to hard, so i using polling 
#TIP: if you use polling, use it in infitity loop construction to add stability to project
if __name__=="__main__":

    while 1:
        
        executor.start_polling(dp,on_startup=create_database(),skip_updates=False)
        #time sleep 4 optimization
        time.sleep(15)

