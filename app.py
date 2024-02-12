
from flask import Flask, render_template,request,redirect,url_for
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import random
import time
import pyttsx3
import algo
from forms import UserInfoForm
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
app = Flask(__name__)
app.config.from_object(__name__)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY




# login form template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/signin.html')
def signin():
    return render_template('signin.html')


@app.route('/signup.html')
def signup():
    return render_template('signup.html')


@app.route('/instructionsPractice.html')
def yoga():
    return render_template('instructionsPractice.html')


@app.route('/learn.html')
def learn():
    return render_template('learn.html')

@app.route('/exercise.html')
def exercise():
    return render_template('exercise.html')


@app.route('/curls.html')
def curls():
    return render_template('curls.html')

@app.route('/tricep.html')
def tricep():
    return render_template('tricep.html')

@app.route('/highknee.html')
def knee():
    return render_template('highknee.html')    

@app.route('/press.html')
def press():
    return render_template('press.html')

@app.route('/squats.html')
def squats():
    return render_template('squats.html')

@app.route('/lateral.html')
def lateral():
     return render_template('lateral.html')
    
@app.route('/dumbell.html')
def dumbell():
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
            
        return angle

    # Dumbbell Press COUNTER

    cap = cv2.VideoCapture(0)

    # Dumbbell Press counter variables
    counter = 0 
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
    # ANGLE 1            
                # Get coordinate vectors for joints
                rt_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rt_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                lt_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                
                # Calculate angle between 3 joints
                angle1 = calculate_angle(lt_shoulder, rt_shoulder, rt_elbow)
                
                # Visualize angle (Print angle on display)
                cv2.putText(image, str(angle1), 
                            tuple(np.multiply(rt_shoulder, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
    # ANGLE 2            
                # Get coordinate vectors for joints
                lt_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lt_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                rt_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                
                # Calculate angle between 3 joints
                angle2 = calculate_angle(rt_shoulder, lt_shoulder, lt_elbow)
                
                # Visualize angle (Print angle on display)
                cv2.putText(image, str(angle2), 
                            tuple(np.multiply(lt_shoulder, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
    # Dumbbell press counter logic
                if angle1 < 135 and angle2 < 135:
                    stage = "down"
                if angle1 > 175 and angle2 > 175 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
                        
            except:
                pass
            
            # Render dumbbell press counter
            # Setup status box
            cv2.rectangle(image, (0,0), (640,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(image, 'REPS', (18,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (100,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (100,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('Dumbbell Press Counter Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('exercise.html')


@app.route('/diet.html',methods=['GET','POST'])
def home():   
	form=UserInfoForm()
	if form.validate_on_submit():
		if request.method=='POST':
			name=request.form['name']
			weight=float(request.form['weight'])
			height=float(request.form['height'])
			age=int(request.form['age'])
			gender=request.form['gender']
			phys_act=request.form['physical_activity']

			tdee=algo.calc_tdee(name,weight,height,age,gender,phys_act)
			return redirect(url_for('result1',tdee=tdee))

	return render_template('diet.html',title="Diet App",form=form)

@app.route('/result1',methods=['GET','POST'])
def result1():
	tdee=request.args.get('tdee')
	if tdee is None:
		return render_template('warriorstart.html',title="Error Page")
	
	tdee=float(tdee)
	breakfast= algo.bfcalc(tdee)
	snack1=algo.s1calc(tdee)
	lunch=algo.lcalc(tdee)
	snack2=algo.s2calc(tdee)
	dinner=algo.dcalc(tdee)
	snack3=algo.s3calc(tdee)
	return render_template('result1.html',title="Result",breakfast=breakfast,snack1=snack1,lunch=lunch,snack2=snack2,dinner=dinner,snack3=snack3)

@app.route('/exerciseplan.html')
def eplan():
    return render_template('exerciseplan.html')

@app.route('/result', methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    name = output["name"]
    age = output["age"]
    weight = output["weight"]
    height = output["height"]
    height1 = int(height)/100
    bmi = round(int(weight) / (height1*height1),2)
    status = 'unknown'
    if bmi <= 18.5:
        status = "Underweight"
    elif bmi>18.5 and bmi<=24.9:
        status = "Healthy Weight"
    elif bmi>=25.0 and bmi<=29.9:
        status = "Overweight"
    else:
        status = "Obesity"
    import random
    k=5
    exercise = ('Pushups','Squats','Burpees','Lunges','Crunches','Rotational jacks','Step-ups','Mountain climbers','Squat jumps',
                'Standing side hops','Pullups','Squat pulses','Flutter kicks','Plank')
    work1 = random.choices(exercise,k=5)
    work2 = random.choices(exercise,k=5)
    work3 = random.choices(exercise,k=5)
    work4 = random.choices(exercise,k=5)
    work5 = random.choices(exercise,k=5)
    work6 = random.choices(exercise,k=5)
    work7 = random.choices(exercise,k=5)
    work8 = random.choices(exercise,k=5)
    work9 = random.choices(exercise,k=5)
    work10 = random.choices(exercise,k=5)
    work11= random.choices(exercise,k=5)
    work12 = random.choices(exercise,k=5)
    work13 = random.choices(exercise,k=5)
    work14 = random.choices(exercise,k=5)
    work15 = random.choices(exercise,k=5)
    reps1 = random.randrange(10,20,1)
    reps2 = random.randrange(10,20,1)
    reps3 = random.randrange(10,20,1)
    reps4 = random.randrange(10,20,1)
    reps5 = random.randrange(10,20,1)
    reps6 = random.randrange(10,20,1)
    reps7 = random.randrange(10,20,1)
    reps8 = random.randrange(10,20,1)
    reps9 = random.randrange(10,20,1)
    reps10 = random.randrange(10,20,)
    reps11 = random.randrange(10,20,1)
    reps12 = random.randrange(10,20,1)
    reps13 = random.randrange(10,20,1)
    reps14 = random.randrange(10,20,1)
    reps15 = random.randrange(10,20,1)
    sets1 = random.randrange(1,5,1)
    sets2 = random.randrange(1,5,1)
    sets3 = random.randrange(1,5,1)
    sets4 = random.randrange(1,5,1)
    sets5 = random.randrange(1,5,1)
    sets6 = random.randrange(1,5,1)
    sets7 = random.randrange(1,5,1)
    sets8 = random.randrange(1,5,1)
    sets9 = random.randrange(1,5,1)
    sets10 = random.randrange(1,5,1)
    sets11 = random.randrange(1,5,1)
    sets12 = random.randrange(1,5,1)
    sets13 = random.randrange(1,5,1)
    sets14 = random.randrange(1,5,1)
    sets15 = random.randrange(1,5,1)
    rest = '30 seconds'
    
    
    return render_template('result.html', name = name, age = age, weight = weight, height = height, bmi = bmi,status=status,  sets1=sets1, rest=rest, reps1= reps1, 
                           work1=work1, work2=work2, work3=work3,work4=work4,work5=work5,work6=work6,work7=work7,work8=work8,work9=work9,work10=work10,work11=work11,work12=work12,work13=work13,work14=work14,work15=work15,
                           reps2= reps2,reps3= reps3,reps4= reps4,reps5= reps5,reps6= reps6,reps7= reps7,reps8= reps8,reps9= reps9,reps10= reps10,reps11= reps11,reps12= reps12,reps13= reps13,reps14= reps14,reps15= reps15,
                           sets2=sets2,sets3=sets3,sets4=sets4,sets5=sets5,sets6=sets6,sets7=sets7,sets8=sets8,sets9=sets9,sets10=sets10,sets11=sets11,sets12=sets12,sets13=sets13,sets14=sets14,sets15=sets15,)

@app.route('/bicepstart.html')
def curlsstart():
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
            
        return angle

    # CURL COUNTER

    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    cal = str(random.randrange(10,20,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
    # ANGLE 1            
                # Get coordinates
                lt_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                lt_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lt_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle1 = calculate_angle(lt_shoulder, lt_elbow, lt_wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle1), 
                            tuple(np.multiply(lt_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
    # ANGLE 2           
                # Get coordinates
                rt_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                rt_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rt_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                # Calculate angle
                angle1 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle2=calculate_angle(rt_shoulder,rt_elbow,rt_wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle1), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                cv2.putText(image, str(angle2), 
                            tuple(np.multiply(rt_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                # Curl counter logic
                if angle1 > 160 and angle2 > 160:
                    stage = "down"
                if angle1 < 30 and angle2 < 30 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
                        
            except:
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'BICEP CURLS', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            if counter >15 :
                        
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )              
            
            cv2.imshow('Curl Counter Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('exercise.html')

@app.route('/tricepstart.html')
def tricepstart():
    def calculate_angle(a,b,c):
        a = np.array(a)  #first angle
        b = np.array(b)  #second angle
        c = np.array(c)  #third angle
        
        radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle>180.0:
            angle = 360-angle
        return angle

    cap = cv2.VideoCapture(0)

    #creating curl counter variable
    counter = 0
    cal = str(random.randrange(10,20,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    stage = None
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate angle
                angle_1 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle_2=calculate_angle(right_shoulder,right_elbow,right_wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle_1), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                cv2.putText(image, str(angle_2), 
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                #CURL COUNTER LOGIC
                if angle_1 > 110 and angle_2 >110 :
                    stage = "Up"

                if angle_1 < 90 and angle_2 < 90 and stage == 'Up':
                    stage = "Down"
                    counter +=1
                     
            except:
                pass
            
            #setting up curl counter box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'TRICEP EXTENTION', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            if counter >15 :
                        
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('VIDEO', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    return render_template('exercise.html')

@app.route('/lateralstart.html')
def lateralstart():
    def calculate_angle(a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
            
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            if angle > 180.0:
                angle = 360-angle
                
            return angle

    # Lateral Raise COUNTER

    cap = cv2.VideoCapture(0)

    # Lateral Raise counter variables
    counter = 0 
    cal = str(random.randrange(10,20,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate angle
                angle_1 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle_2=calculate_angle(right_shoulder,right_elbow,right_wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle_1), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                cv2.putText(image, str(angle_2), 
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
    # Lateral Raise counter logic for both arms
                if angle_1 < 20 and angle_2 < 20:
                    stage = "down"
                if angle_1 > 90 and angle_2 > 90 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
                        
            except:
                pass
            
                       #setting up curl counter box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'LATERAL RAISES', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            if counter >15 :
                        
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )        
            
            cv2.imshow('Lateral Raise Counter Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('exercise.html')

@app.route('/pressstart.html')
def pressstart():
    def calculate_angle(a,b,c):
        a = np.array(a)  #first angle
        b = np.array(b)  #second angle
        c = np.array(c)  #third angle
        
        radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle>180.0:
            angle = 360-angle
        return angle

    cap = cv2.VideoCapture(0)

    #creating curl counter variable
    counter = 0
    cal = str(random.randrange(10,20,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    stage = None
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                # Calculate angle
                angle_1 = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle_2=calculate_angle(right_shoulder,right_elbow,right_wrist)
                
                # Visualize angle
                cv2.putText(image, str(angle_1), 
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                cv2.putText(image, str(angle_2), 
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                #CURL COUNTER LOGIC
                if angle_1 > 110 and angle_2 >110 :
                    stage = "Up"

                if angle_1 < 90 and angle_2 < 90 and stage == 'Up':
                    stage = "Down"
                    counter +=1
                     
            except:
                pass
            
            #setting up curl counter box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'SHOULDER PRESS', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            if counter >15 :
                        
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('VIDEO', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    return render_template('exercise.html')


@app.route('/kneestart.html')
def kneestart():
    def calculate_angle(a,b,c):
        a = np.array(a)  #first angle
        b = np.array(b)  #second angle
        c = np.array(c)  #third angle
        
        radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle>180.0:
            angle = 360-angle
        return angle

    #Curl Counter


    cap = cv2.VideoCapture(0)

    #creating curl counter variable
    counter = 0
    cal = str(random.randrange(30,50,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    stage = None
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                
                # Calculate angle
                angle = calculate_angle(shoulder, hip, knee)
                
                # Visualize angle
                cv2.putText(image, str(angle), 
                            tuple(np.multiply(hip, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                #CURL COUNTER LOGIC
                if angle > 160:
                    stage = "Down"
                if angle < 80 and stage == 'Down':
                    stage = "Up"
                    counter +=1
                    print(counter)

                        
            except:
                pass
            
            #setting up curl counter box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'HIGH KNEES', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            if counter >30 :
                
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                    
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('VIDEO', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('exercise.html')

@app.route('/squatsstart.html')
def squatsstart():
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
            
        return angle

    # SQUATS COUNTER

    cap = cv2.VideoCapture(0)

    # Squat counter variables
    cal = str(random.randrange(10,20,2))
    cal1 = 'Clories Burned: {}'.format(cal)
    counter = 0 
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

    # ANGLE 1            
                # Get coordinate vectors for joints
                rt_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rt_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                rt_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # Calculate angle between 3 joints
                angle1 = calculate_angle(rt_hip, rt_knee, rt_ankle)
                
                # Visualize angle (Print angle on display)
                cv2.putText(image, str(angle1), 
                            tuple(np.multiply(rt_knee, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
    # ANGLE 2
                # Get coordinate vectors for joints
                lt_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                lt_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                lt_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                # Calculate angle between 3 joints
                angle2 = calculate_angle(lt_hip, lt_knee, lt_ankle)
                
                # Visualize angle (Print angle on display)
                cv2.putText(image, str(angle2), 
                            tuple(np.multiply(lt_knee, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                
    # Squats counter logic
                if angle1 < 100 and angle2 < 100:
                    stage = "down"
                if angle1 > 175 and angle2 > 175 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
                        
            except:
                pass
            
            # Render squats counter
            # Setup status box
            cv2.rectangle(image, (0,0), (360,72), (245,117,16), -1)
            
            #sending values to curl counter box
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            #printing hand stage while exercising
            
            cv2.putText(image, 'STAGE', (165,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (165,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, 'SQUATS', (390,18), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            if counter >15 :
                        
                        cv2.rectangle(image, (40,200), (600,72), (255,255,255), -1)
                        cv2.putText(image,cal1, (60,150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 1, cv2.LINE_AA)
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
                 
            
            cv2.imshow('SQUATS Counter Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('exercise.html')

@app.route('/tree.html')
def tree():
     return render_template('tree.html')

@app.route('/tpose.html')
def tpose():
     return render_template('tpose.html')

@app.route('/warrior.html')
def warrior():
     return render_template('warrior.html')

@app.route('/treestart.html')
def treestart():
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End         
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)          
        if angle >180.0:
            angle = 360-angle     
        return angle

    cap = cv2.VideoCapture(0)

    #Creating lable variable
    label="Unknown Pose"

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            ##STEP I 
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_shoulder= [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # STEP II:Calculate angle between the joints
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle=calculate_angle(right_shoulder,right_elbow,right_wrist)
                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
                left_hip_angle=calculate_angle(left_knee,left_hip,left_shoulder)
                right_hip_angle=calculate_angle(right_knee,right_hip,right_shoulder)
                left_knee_angle=calculate_angle(left_ankle,left_knee,left_hip)
                right_knee_angle=calculate_angle(right_ankle,right_knee,right_hip)
            
                #STEP III: Classifing poses
                #Check if hands are staright or not
                #Tree Pose
                if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195 :
                    if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45 :
                        label = 'Tree Pose'
                        #text2speech("treepose.txt")
                        
                else:
                    label = 'Unknown Pose'
            
            except:
                pass
            
            #Showing label on the output screen
            cv2.putText(image, label,(10,60),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 1, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
                    
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render_template('tree.html')

@app.route('/warriorstart.html')
def warriorstart():
    import cv2
    import mediapipe as mp
    import numpy as np
    import pyttsx3
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose 

    engine = pyttsx3.init()
        #def text2speech(text_file):
            #pose=text_file
            #f=open(pose,'r')
            #text=f.read()
            ##f.close()
            #engine.setProperty('rate',150)
        # engine.say(text)
            #engine.runAndWait()

        #Function to calculate angles between two bones which will be used further.
    def calculate_angle(a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
            
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            
            if angle >180.0:
                angle = 360-angle
                
            return angle

    cap = cv2.VideoCapture(0)

        #Creating lable variable
    label="Unknown Pose"

        # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                
                ##STEP I 
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinates
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    right_shoulder= [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    # STEP II:Calculate angle between the joints
                    left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_elbow_angle=calculate_angle(right_shoulder,right_elbow,right_wrist)
                    left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                    right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
                    left_hip_angle=calculate_angle(left_knee,left_hip,left_shoulder)
                    right_hip_angle=calculate_angle(right_knee,right_hip,right_shoulder)
                    left_knee_angle=calculate_angle(left_ankle,left_knee,left_hip)
                    right_knee_angle=calculate_angle(right_ankle,right_knee,right_hip)
                
                    #STEP III: Classifing poses
                    #Check if hands are staright or not
                    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
                        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
                            #Warrior II pose
                            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:
                                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:
                                    label="warrior II Pose"
                                    #text2speech("Warrior_II.txt")
                            
                    else:
                        label = 'Unknown Pose'
                
                except:
                    pass
                
                #Showing label on the output screen
                cv2.putText(image, label,(10,60),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 1, cv2.LINE_AA)
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
                        
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
    return render_template('warrior.html')

@app.route('/tposestart.html')
def tposestart():


#Function to calculate angles between two bones which will be used further.
    def calculate_angle(a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle

    cap = cv2.VideoCapture(0)

    #Creating lable variable
    label="Unknown Pose"

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            ##STEP I 
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_shoulder= [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # STEP II:Calculate angle between the joints
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle=calculate_angle(right_shoulder,right_elbow,right_wrist)
                left_shoulder_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
                right_shoulder_angle = calculate_angle(right_hip, right_shoulder, right_elbow)
                left_hip_angle=calculate_angle(left_knee,left_hip,left_shoulder)
                right_hip_angle=calculate_angle(right_knee,right_hip,right_shoulder)
                left_knee_angle=calculate_angle(left_ankle,left_knee,left_hip)
                right_knee_angle=calculate_angle(right_ankle,right_knee,right_hip)
            
                #STEP III: Classifing poses
                #Check if hands are staright or not
                if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:
                    if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:
                        if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:
                            label = 'T Pose'    
                            #text2speech("TPose.txt")
                else:
                    label = 'Unknown Pose'
            
            except:
                pass
            
            #Showing label on the output screen
            cv2.putText(image, label,(10,60),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 1, cv2.LINE_AA)
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
                    
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    return render_template('tpose.html')
if __name__ == '__main__':
    app.run(debug = True) 