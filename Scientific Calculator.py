from tkinter import *
import re
import math
from nltk.corpus import stopwords
import speech_recognition as sr
import pyttsx3

stop = stopwords.words('english')

ws = Tk()

ws.title("Scientific Calculator")

ws.geometry("367x430")
ws.minsize(367, 430)
ws.maxsize(367, 430)
ws['bg'] = '#ffffff'


def convert_to_numbers(s):
    words_to_numbers = {
        'one': '1',
        'oneplus': '1+',
        'two': '2',
        'to': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0',
        'ten': '10',
        'hundred': '100',
        'thousand': '1000',
        'plus': '+',
        'minus': '-',
        'dash': '-',
        'add': '+',
        'multiplied by': '*',
        'cross': '*',
        'power': '**',
        '^': '**',
        'square': '**2',
        'cube': '**3',
        'divided by': '/',
        'equal to': '=',
        'equals to': '=',
        'equals': '=',
        'x': '*',
        'X': '*',
        'into': '*',
        'degrees': '',
        'sign': 'sin',
        'sain': 'sin',
        'route': 'root',
        'routine': 'root 10',
        'cause': 'cos',
        'cost': 'cos'
    }

    pattern = re.compile(r'\b(' + '|'.join(words_to_numbers.keys()) + r')\b')
    s = re.sub(pattern, lambda x: words_to_numbers.get(x.group(), ''), s)
    pattern = re.compile(r'\b(' + '|'.join(stop) + r')\b')
    s = re.sub(pattern, '', s)
    s = s.replace('  ', ' ')
    pattern = re.compile(r"√\d+(?:\.\d+)*")
    s = re.sub(pattern, lambda x: str(eval(x.group().replace('√', '')) ** 0.5), s)
    pattern = re.compile(r'\s?sin\s?\d+(?:\.\d+)*\s?')
    s = re.sub(pattern, lambda x: "sin({0})".format(*re.findall(r'\d+(?:\.\d+)*', x.group())), s)
    pattern = re.compile(r'\s?cos\s?\d+(?:\.\d+)*\s?')
    s = re.sub(pattern, lambda x: "cos({0})".format(*re.findall(r'\d+(?:\.\d+)*', x.group())), s)
    pattern = re.compile(r'\s?tan\s?\d+(?:\.\d+)*\s?')
    s = re.sub(pattern, lambda x: "tan({0})".format(*re.findall(r'\d+(?:\.\d+)*', x.group())), s)
    pattern = re.compile(r'\s?log\s\d+\sbase\s\d+\s?')
    s = re.sub(pattern, lambda x: "logX({0},{1})".format(re.findall(r'\d+(?:\.\d+)*', x.group())[0],
                                                         re.findall(r'\d+(?:\.\d+)*', x.group())[1]), s)
    pattern = re.compile(r'\s?log\s?\d+(?:\.\d+)*\s?')
    s = re.sub(pattern, lambda x: "log({0})".format(*re.findall(r'\d+(?:\.\d+)*', x.group())), s)
    pattern = re.compile(r'\s?root\s\d+\sbase\s\d+\s?')
    s = re.sub(pattern, lambda x: "root({0},{1})".format(re.findall(r'\d+(?:\.\d+)*', x.group())[0],
                                                         re.findall(r'\d+(?:\.\d+)*', x.group())[1]), s)
    pattern = re.compile(r'\s?root\s\d+\s?')
    s = re.sub(pattern, lambda x: "root({0},2)".format(re.findall(r'\d+(?:\.\d+)*', x.group())[0]), s)
    pattern = re.compile(r"(?:\(\d+(?:\.\d+)*\)|\d+(?:\.\d+)*)%\s+\d+")
    s = re.sub(pattern, lambda x: f"{(int(x.group().replace('%', '').split()[0]) / 100)*int(x.group().replace('%', '').split()[1]) }", s)
    pattern = re.compile(r"(?:\(\d+(?:\.\d+)*\)|\d+(?:\.\d+)*)%")
    s = re.sub(pattern, lambda x: f"{int(x.group().replace('%', '')) / 100}", s)

    pattern = re.compile(r"\b(?!sin|cos|tan|log|root|\d+(?:\.\d+)*|\s\b)\w+")
    s = re.sub(pattern, lambda x: '', s)

    return s


def primitive_replacement(s):
    words_to_numbers = {
        'audition': 'addition',
        'additional': 'addition',

    }
    pattern = re.compile(r'\b(' + '|'.join(words_to_numbers.keys()) + r')\b')
    s = re.sub(pattern, lambda x: words_to_numbers.get(x.group(), ''), s)
    return s

x_aling = 7
y_aling = 20
Label(ws, text="Speech Calculator", font=('Terminal', 20, 'bold'), fg='#000', bg='#fff', width=20, height=1,
      justify=CENTER).place(x=0, y=15)

tb = Entry(ws, font='Calibri 25', relief='solid', fg="#ffffff", width=20, justify='right', insertbackground='red',
           background="#090909")

tb.place(x=10, y=60)
tb.insert(INSERT, "0")


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return x / y


def sin(x):
    return math.sin(math.radians(x))


def cos(x):
    return math.cos(math.radians(x))


def tan(x):
    return math.tan(math.radians(x))


def log(x):
    return math.log(x)


def logX(*x):
    return math.log(x[0], x[1])


def root(*x):
    return (x[0]) ** (1 / x[1])


def root2(x):
    return x ** (1 / 2)


def root3(x):
    return x ** (1 / 3)





def SpeakText(command):
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)
    engine.say(command)
    engine.runAndWait()


def open_popup():
    top = Toplevel(ws)
    top.geometry("367x430")
    top.minsize(367, 430)
    top.maxsize(367, 430)
    top.title("Speech recognition")
    tbpop = Text(top, font=('Courier New', 13, 'bold'), relief='groove', fg="#000", width=33, height=16,
                 background="#fff", wrap='word')

    tbpop.place(x=17, y=10)
    tbpop.configure(state='disabled')
    label = Label(top, font=('Courier New', 15, "italic"), fg='#ff0000', width=13, height=1)
    label.place(x=10, y=335)

    tbpop.tag_config("question", foreground="black")
    tbpop.tag_config("ans", foreground="green")
    tbpop.tag_config("err", foreground="red")

    def speech_rec():
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.5)
                audio2 = r.listen(source2, phrase_time_limit=7)
                mytext = r.recognize_google(audio2)
                mytext = mytext.lower()
                mytext = primitive_replacement(mytext).replace('°', '')
                _mytext = mytext
                if mytext.find('addition') != -1:
                    try:
                        mytext = mytext[mytext.find('addition'):].replace('+', '')
                        mytext = list(convert_to_numbers(mytext).split())
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {mytext[-2]}+{mytext[-1]} = {round(eval(mytext[-2]) + eval(mytext[-1]), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(10, lambda: SpeakText(_outp.replace('R: ', '')))

                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('subtraction') != -1:
                    try:
                        mytext = mytext[mytext.find('subtraction'):].replace('-', '')
                        mytext = list(convert_to_numbers(mytext).split())
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {mytext[-2]}-{mytext[-1]} = {round(eval(mytext[-2]) - eval(mytext[-1], 2))}\n"
                        tbpop.insert(END, str(_outp))
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('multiplication') != -1:
                    try:
                        mytext = mytext[mytext.find('multiplication'):].replace('*', '')
                        mytext = list(convert_to_numbers(mytext).split())
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {mytext[-2]}*{mytext[-1]} = {round(eval(mytext[-2]) * eval(mytext[-1]), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('division') != -1:
                    try:
                        mytext = mytext[mytext.find('division'):].replace('/', '')
                        mytext = list(convert_to_numbers(mytext).split())
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {mytext[-2]}/{mytext[-1]} = {round(eval(mytext[-2]) / eval(mytext[-1]), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('cube root') != -1:
                    try:
                        mytext = mytext[mytext.find('cube root'):]
                        mytext = list(convert_to_numbers(mytext).split())
                        pattern = re.compile(r'\D')
                        mytext[-1] = re.sub(pattern, lambda x: '', mytext[-1])
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: ∛{mytext[-1]} = {round(root(eval(mytext[-1]), 3), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('square root') != -1:
                    try:
                        mytext = mytext[mytext.find('square root'):]
                        mytext = list(convert_to_numbers(mytext).split())
                        pattern = re.compile(r'\D')
                        mytext[-1] = re.sub(pattern, lambda x: '', mytext[-1])
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: √{mytext[-1]} = {round(root(eval(mytext[-1]), 2), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')


                elif mytext.find('evaluate') != -1:
                    try:
                        mytext = mytext[mytext.find('evaluate'):]
                        mytext = list(convert_to_numbers(mytext).split("equation"))
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {mytext[-1]} = {round(eval(mytext[-1]), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')

                else:
                    try:
                        mytext = [i for i in convert_to_numbers(mytext).split() if not i.isalpha()]
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"Q: {_mytext}\n")
                        tbpop.tag_add("question", f"end-{3 + len(_mytext)}c", "end-1c")
                        _outp = f"R: {''.join(mytext)} = {round(eval(''.join(mytext)), 2)}\n"
                        tbpop.insert(END, _outp)
                        tbpop.tag_add("ans", f"end-{1 + len(_outp)}c", "end-1c")
                        tbpop.configure(state='disabled')
                        top.after(100, lambda: SpeakText(_outp.replace('R: ', '')))
                    except Exception as e:
                        tbpop.configure(state='normal')
                        tbpop.insert(END, f"R: !!!!ERROR Try Again!!!!\n")
                        tbpop.tag_add("err", f"end-{5 + len('!!!!ERROR Try Again!!!!')}c", "end-1c")
                        tbpop.configure(state='disabled')

                # tbpop.configure(state='normal')
                # tbpop.insert(END, f"Q: {_mytext}\n")
                # tbpop.tag_add("question", f"end-{3+len(_mytext)}c", "end-1c")
                # tbpop.insert(END, f"R: Answer\n")
                # tbpop.tag_add("ans", f"end-{3+len('R: Answer')}c", "end-1c")
                # tbpop.configure(state='disabled')
        except sr.RequestError as e:
            tbpop.configure(state='normal')
            tbpop.insert(END, "A: Connect To the Internet\n")
            tbpop.tag_add("err", f"end-{3 + len('A: !!!Connect To the Internet!!!')}c", "end-1c")
            tbpop.configure(state='disabled')
        except sr.UnknownValueError:
            tbpop.configure(state='normal')
            tbpop.insert(END, f"Q: Not Recognized\n")
            tbpop.tag_add("question", f"end-{3 + len('Q: Not Recognized')}c", "end-1c")
            tbpop.insert(END, f"F: Try Again\n")
            tbpop.tag_add("err", f"end-{3 + len('E: Try Again')}c", "end-1c")
            tbpop.configure(state='disabled')
        label.configure(text="")
        btnn.configure(fg="#000")
        tbpop.see("end")

    def update_text():
        label.configure(text="Listening...")
        btnn.configure(fg="#ff0000")
        top.after(50, lambda: speech_rec())

    btnn = Button(top, text=chr(int('0x0001F399', 16)), font=('Calibri 20'), width=3, height=1, command=update_text)
    btnn.place(x=160, y=360)


def fun(val):
    equl.focus_set()
    if (tb.get() == 'ERROR'):
        tb.delete(0, 'end')
    if (tb.get() == '0'):
        tb.delete(0, 1)
    try:
        _txt = tb.get()
        i = 0
        while (i < len(_txt) and (_txt[~i].isnumeric() or _txt[~i] == '.')):
            i += 1
        if (eval(_txt[~i:]) and re.findall(r"^(?:sin|cos|tan|log)\(\s\)$", val)):
            val = val.replace(' ', str(eval(_txt[~i:])))
            tb.delete(len(_txt) - i, 'end')
            tb.insert(INSERT, val)
            return
        if (eval(_txt[~i:]) and re.findall(r"^logX\(\s,[1-9]+\d*(?:\.\d*[1-9]+)*\)$", val)):
            val = val.replace(' ', str(eval(_txt[~i:])))
            tb.delete(len(_txt) - i, 'end')
            tb.insert(INSERT, val)
            return
        if (eval(_txt[~i:]) and re.findall(r"^\(\s\)\^(?:\(\d+\)|\d+)$", val)):
            val = val.replace(' ', str(eval(_txt[~i:])))
            tb.delete(len(_txt) - i, 'end')
            tb.insert(INSERT, val)
            return
        if (eval(_txt[~i:]) and re.findall(r"^\(\s\)\^\(\s\)$", val)):
            val = val.replace(' ', str(eval(_txt[~i:])), 1)
            tb.delete(len(_txt) - i, 'end')
            tb.insert(INSERT, val)
            return
    except Exception:
        pass
    tb.insert(INSERT, val)
    tb.xview_scroll(len(tb.get()), UNITS)


def backspace():
    # if(tb.selection_present()):
    #     _txt = tb.get()
    #
    #     _txt=_txt.replace(tb.selection_get(),'',1)
    #     tb.delete(0, 'end')
    #     tb.insert(INSERT, _txt)
    # else:
    equl.focus_set()
    pos = tb.index(INSERT)
    pos = int(pos)
    _txt = tb.get()
    if (_txt and not _txt[pos - 1].isalpha()):
        tb.delete(f"{pos - 1}", f"{pos}")
    else:
        i = pos
        while (i > 0 and _txt[i - 1].isalpha()):
            i -= 1
        tb.delete(f"{pos - (len(_txt) - i)}", f"{pos}")


def evaluate():
    equl.focus_set()
    try:
        _txt = tb.get().replace('x', '*').replace('^', '**').replace(' ', '')
        tb.delete(0, 'end')
        pattern = re.compile(r"0+[1-9]+")
        _txt = re.sub(pattern, lambda x: f"{x.group().replace('0', '')}", _txt)
        pattern = re.compile(r"√\d+(?:\.\d+)*")
        _txt = re.sub(pattern, lambda x: f"root2({x.group().replace('√', '')})", _txt)
        pattern = re.compile(r"∛\d+(?:\.\d+)*")
        _txt = re.sub(pattern, lambda x: f"root3({x.group().replace('∛', '')})", _txt)
        pattern = re.compile(r"(?:\(\d+(?:\.\d+)*\)|\d+(?:\.\d+)*)%")
        _txt = re.sub(pattern, lambda x: f"{int(x.group().replace('%', '').replace('(', '').replace(')', '')) / 100}",
                      _txt)
        _x = eval(_txt)
        if _x - int(_x):
            tb.insert(INSERT, round(_x, 2))
        else:
            tb.insert(INSERT, str(int(_x)))
    except Exception:
        tb.insert(INSERT, 'ERROR')


def left():
    tb.focus_set()
    tb.icursor(tb.index(INSERT))


def right():
    tb.focus_set()
    tb.icursor(tb.index(INSERT))


ws.bind('<Return>', lambda event: evaluate())
for i in range(10):
    ws.bind(i, lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun(event.char))
ws.bind('<BackSpace>', lambda event: backspace())
ws.bind('+', lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun(event.char))
ws.bind('-', lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun(event.char))
ws.bind('/', lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun(event.char))
ws.bind('*', lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun('x'))
ws.bind('.', lambda event: equl.focus_set() if (str(tb.focus_get()) == '.!entry') else fun(event.char))
ws.bind('<Left>', lambda eve: left())
ws.bind('<Right>', lambda eve: right())
Button(ws, text="log", font=('Calibri 18'), width=5, height=1, command=lambda: fun('log( )')).place(x=x_aling + 0,
                                                                                                    y=y_aling + 95)
Button(ws, text="logx", font=('Calibri 18'), width=5, height=1, command=lambda: fun('logX( ,10)')).place(x=x_aling + 70,
                                                                                                         y=y_aling + 95)
Button(ws, text="(", font=('Calibri 18'), width=2, height=1, command=lambda: fun('(')).place(x=x_aling + 140,
                                                                                             y=y_aling + 95)
Button(ws, text=")", font=('Calibri 18'), width=2, height=1, command=lambda: fun(')')).place(x=x_aling + 176,
                                                                                             y=y_aling + 95)
Button(ws, text="AC", font=('Calibri 18'), width=5, height=1, command=lambda: tb.delete(0, 'end')).place(
    x=x_aling + 210, y=y_aling + 95)
Button(ws, text="⌫", font=('Calibri 18'), width=5, height=1, command=backspace).place(x=x_aling + 280, y=y_aling + 95)
Button(ws, text="sin", font=('Calibri 18'), width=5, height=1, command=lambda: fun('sin( )')).place(x=x_aling + 0,
                                                                                                    y=y_aling + 146)
Button(ws, text="cos", font=('Calibri 18'), width=5, height=1, command=lambda: fun('cos( )')).place(x=x_aling + 70,
                                                                                                    y=y_aling + 146)
Button(ws, text="tan", font=('Calibri 18'), width=5, height=1, command=lambda: fun('tan( )')).place(x=x_aling + 140,
                                                                                                    y=y_aling + 146)
Button(ws, text="%", font=('Calibri 18'), width=5, height=1, command=lambda: fun('%')).place(x=x_aling + 210,
                                                                                             y=y_aling + 146)
Button(ws, text="/", font=('Calibri 18'), width=5, height=1, command=lambda: fun('/')).place(x=x_aling + 280,
                                                                                             y=y_aling + 146)
Button(ws, text="7", font=('Calibri 18'), width=5, height=1, command=lambda: fun('7')).place(x=x_aling + 0,
                                                                                             y=y_aling + 197)
Button(ws, text="8", font=('Calibri 18'), width=5, height=1, command=lambda: fun('8')).place(x=x_aling + 70,
                                                                                             y=y_aling + 197)
Button(ws, text="9", font=('Calibri 18'), width=5, height=1, command=lambda: fun('9')).place(x=x_aling + 140,
                                                                                             y=y_aling + 197)
Button(ws, text="√", font=('Calibri 18'), width=5, height=1, command=lambda: fun('√')).place(x=x_aling + 210,
                                                                                             y=y_aling + 197)
Button(ws, text="x", font=('Calibri 18'), width=5, height=1, command=lambda: fun('x')).place(x=x_aling + 280,
                                                                                             y=y_aling + 197)
Button(ws, text="4", font=('Calibri 18'), width=5, height=1, command=lambda: fun('4')).place(x=x_aling + 0,
                                                                                             y=y_aling + 248)
Button(ws, text="5", font=('Calibri 18'), width=5, height=1, command=lambda: fun('5')).place(x=x_aling + 70,
                                                                                             y=y_aling + 248)
Button(ws, text="6", font=('Calibri 18'), width=5, height=1, command=lambda: fun('6')).place(x=x_aling + 140,
                                                                                             y=y_aling + 248)
Button(ws, text="∛", font=('Calibri 18'), width=5, height=1, command=lambda: fun('∛')).place(x=x_aling + 210,
                                                                                             y=y_aling + 248)
Button(ws, text="-", font=('Calibri 18'), width=5, height=1, command=lambda: fun('-')).place(x=x_aling + 280,
                                                                                             y=y_aling + 248)
Button(ws, text="1", font=('Calibri 18'), width=5, height=1, command=lambda: fun('1')).place(x=x_aling + 0,
                                                                                             y=y_aling + 299)
Button(ws, text="2", font=('Calibri 18'), width=5, height=1, command=lambda: fun('2')).place(x=x_aling + 70,
                                                                                             y=y_aling + 299)
Button(ws, text="3", font=('Calibri 18'), width=5, height=1, command=lambda: fun('3')).place(x=x_aling + 140,
                                                                                             y=y_aling + 299)
Button(ws, text="x²", font=('Calibri 18'), width=5, height=1, command=lambda: fun('( )^2')).place(x=x_aling + 210,
                                                                                                  y=y_aling + 299)
Button(ws, text="+", font=('Calibri 18'), width=5, height=1, command=lambda: fun('+')).place(x=x_aling + 280,
                                                                                             y=y_aling + 299)
Button(ws, text=chr(int('0x0001F399', 16)), font=('Calibri 18'), width=5, height=1, command=open_popup).place(
    x=x_aling + 0, y=y_aling + 350)
Button(ws, text="0", font=('Calibri 18'), width=5, height=1, command=lambda: fun('0')).place(x=x_aling + 70,
                                                                                             y=y_aling + 350)
Button(ws, text=".", font=('Calibri 18'), width=5, height=1, command=lambda: fun('.')).place(x=x_aling + 140,
                                                                                             y=y_aling + 350)
Button(ws, text="xⁿ", font=('Calibri 18'), width=5, height=1, command=lambda: fun('( )^( )')).place(x=x_aling + 210,
                                                                                                    y=y_aling + 350)
equl = Button(ws, text="=", font=('Calibri 18'), width=5, height=1, command=evaluate)
equl.place(x=x_aling + 280, y=y_aling + 350)
equl.focus_set()
ws.mainloop()
