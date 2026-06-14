import streamlit as st
import random, time

spelldata=[["naive","naieve","nave","niave","nieve"],
           ["prove","proove","proov","proofe","porove"],
           ["particular","particuler","partacular","particulier","particuliar"],
           ["specific","spacefic","spacific","specefic","spacifec"],
           ["advocate","advacate","addvocate","addvacate","advocote"],
           ["unequivocal","inequivocal","anequivocal","unequivacal","unequivocale"],
           ["psychological","pyschological","psychalogical","pychological","psychelogical"],
           ["receive","recieve","receeve","reseive","recive"],
           ["physiological","physialogical","phsyiological","pyhsiological","phisyological"],
           ["despondent","despondant","dispondent","dispondant","depsondent"],
           ["callous","callouse","calous","calouse","callus"]
           ]
spellqs=[]
for spellingset in spelldata:
    correct=spellingset[0]
    random.shuffle(spellingset)
    spellqs.append({"correct":correct,"options":spellingset})
qs=5 #default number of questions

def nl(num_of_lines):
     for i in range(num_of_lines):
         st.write(" ")

def btn_click():
    ss.counter+=1
    if ss.counter>=len(ss.button_label):
        ss.counter=0
        ss.clear()
    else:
        update_session_state()
        #with st.spinner("*this may take a while*"):
        #    time.sleep(0.1)

def update_session_state():
    if ss.counter==1:
        ss['start'] = True
        ss['stop']=False
        ss.current_quiz=random.sample(spellqs,ss.qs)
        ss['button_label'] = ['Start'] + ['Submit', 'Next'] * ss.qs + ['Reload']
        ss.current=0
        ss['starttime']=time.time()
    elif ss.counter==len(ss.button_label)-1:
        ss['start']=False
        ss['stop']=False
        ss['complete']=True
        ss['endtime']=time.time()
    elif ss.counter%2==1:
        #odd number of clicks
        ss['start']=True
        ss['stop']=False
        ss.current+=1
    else:
        #even number of clicks
        ss['start']=False
        ss['stop']=True

def quiz_app():
#create container
    #with st.container():
    if ss.start or ss.stop:

        current_question=ss.current+1
        number_placeholder.write(f"**Question {current_question}: Choose the correct spelling and click submit**")
        options=ss.current_quiz[ss.current].get("options")
        options_placeholder.radio("",options,index=None,key=f"Q{ss.current}")
        nl(1)
    if ss.stop:
        correct_answer=ss.current_quiz[ss.current].get("correct")
        if ss[f'Q{ss.current}'] == correct_answer:
            ss.user_answers[ss.current]=True
            results_placeholder.success("Correct")
        else:
            ss.user_answers[ss.current]=False
            results_placeholder.error(f"Incorrect.  The correct spelling is **{correct_answer}**")

    if ss.complete:
        ss['grade'] = list(ss.user_answers.values()).count(True)
        ss['timetaken']=round(ss['endtime']-ss['starttime'])
        if ss['grade']>0:
            averagetime=round(ss['timetaken']/ss['grade'])
        else:
            averagetime="Inf"
        scorecard_placeholder.write(f"### **Your final score : {ss['grade']} / {len(ss.current_quiz)}**\n### **Your total time : {ss['timetaken']}s**\n### **Average time: {averagetime}s**")

#activate session state to maintain state across refreshes
ss=st.session_state
#initialise variables
if 'counter' not in ss:
    ss['counter']=0
if 'current' not in ss:
    ss['current']=0
if 'start' not in ss:
    ss['start']=False
if 'stop' not in ss:
    ss['stop']=False
if 'complete' not in ss:
    ss['complete']=False
if 'starttime' not in ss:
    ss['starttime']=False
if 'endtime' not in ss:
    ss['endtime']=False
if 'button_label' not in ss:
    ss['button_label']=['Start']+['Submit','Next']*qs +['Reload']
if 'current_quiz' not in ss:
    ss['current_quiz']=[]
if 'user_answers' not in ss:
    ss['user_answers']={}
if 'grade' not in ss:
    ss['grade']=0
if 'timetaken' not in ss:
    ss['timetaken']=0
if 'qs' not in ss:
    ss['qs']=qs


st.title("Julie's Spelling Bee")
nl(1)
st.header("How good is your spelling?")
nl(1)
with st.container():
    instructions_placeholder=st.empty()
    questionnumber_placeholder=st.empty()
    error_placeholder=st.empty()
if not ss['start'] and not ss['stop'] and not ss['complete']:
    try:

        qs=int(questionnumber_placeholder.text_input("How many questions?",ss.qs))
        if qs<1 or qs>10:
            raise ValueError
        else:
            ss.qs=qs
    except:
        error_placeholder.error("Please only enter numeric values between 1 and 10")

if not ss['start']:
    instructions_placeholder.write(f"""
        There will be {ss.qs} questions.
        For each question, select the correct spelling from the 5 options and click submit.
        Then click next to take you to the next question or finish the quiz.
    
        Click start or reload to begin
    """)

#placeholder to print score
scorecard_placeholder=st.empty()
with st.container():
    number_placeholder = st.empty()
    options_placeholder = st.empty()
    results_placeholder = st.empty()



st.button(label=ss.button_label[ss.counter],key='button_press',on_click=btn_click)
quiz_app()




