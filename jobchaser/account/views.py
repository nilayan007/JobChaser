from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import AlgorithmInputSerializer, UserProfileUpdateSerializer, UserRegistrationSerializer , UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,AlgorithmViewSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import csv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# token generator
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
#registration api 
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]  
    def post(self,request,format=None):
        
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user) #generating token
        return Response({'token':token,'msg':'registration success'},status = status.HTTP_201_CREATED)
      

    
    
#userloginapi
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None :
            token = get_tokens_for_user(user) #generating token
            return Response({'token':token,'msg':'login success'},status = status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['email or password is not valid ']}},status = status.HTTP_401_UNAUTHORIZED)
        
    
#user profile view   api
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]  
    permission_classes = [IsAuthenticated]  
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        #if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)
    
# change password api 
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]  
    permission_classes = [IsAuthenticated]   
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})        
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'password change succesfully'},status = status.HTTP_200_OK)
       
#reset password link in gmail api
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password reset link send, please check your email'},status=status.HTTP_200_OK)
        
        
# update new password via mail
class UserPasswordResetView(APIView):
    def post(self,request,uid,token,format=None):
        serializers = UserPasswordResetSerializer(data=request.data, context={'uid':uid,'token':token})
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'password reset succesfully'},status = status.HTTP_200_OK)     

#ML algo using
class AlgorithmView(APIView):
    renderer_classes = [UserRenderer]  
    permission_classes = [IsAuthenticated]  
    def get(self,request,format=None):
        serializer = AlgorithmViewSerializer(request.user)
        #if serializer.is_valid():
    
       
        skills11 = serializer.data.get('skill')
        split_string = [word.strip() for word in skills11.split(",")]
        skills1 = ",".join(split_string)
        print(skills1)
        user_exp = serializer.data.get('yoe')
        original_skills = skills1.split(',')
        user_skills =  [item.upper() for item in original_skills]
        print(user_exp)
        print(user_skills)
        # Read the CSV file
        csv_file_path = "./account/dataset/jobss.csv"
       
        try:
          
            data = pd.read_csv(csv_file_path, encoding="utf8")
            if data is None:
                raise ValueError("Failed to load CSV data")

            # Explicitly replace NaN values with an empty string
            data['required_skills'] = data['required_skills'].fillna('')
            
            
        
            # ALGORITHM LOGIC STARTS
            jobs = data['job_post']
        
            skills = data['required_skills']
            #print(jobs) 
        
            data['required_skills'] = data['required_skills'].str.upper()
        
            data.drop(data.columns[[0]],axis=1 ,inplace=True)
        
            #data['Needed_Exp'] = data['Needed_Exp'].astype(int)
        
            #data['Needed_Exp'].unique().astype(int)
            vectorizer=TfidfVectorizer()
                     
            skill_vectors=vectorizer.fit_transform(skills)
            for i in range(len(user_skills)):
                if user_skills[i] == "C":
                    user_skills[i] = "C LANGUAGE"
                elif user_skills[i] == "C++":
                    user_skills[i] = "CPP"
                elif user_skills[i]=="R":
                    user_skills[i]="MATLAB"
                elif user_skills[i]=="C#":
                    user_skills[i]="C HAS"  
                elif user_skills[i]=="CORE JAVA":
                    user_skills[i]="JAVA"
                elif user_skills[i]=="NODE.JS":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="NODE JS":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="NODE":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="REACT.JS":
                    user_skills[i]="REACTJS"
                elif user_skills[i]=="REACT JS":
                    user_skills[i]="REACTJS"
                elif user_skills[i]=="REACT":
                    user_skills[i]="REACTJS"       
 
            user_vector = vectorizer.transform(user_skills)
            
            type(user_skills)
            
            similarities = cosine_similarity(user_vector, skill_vectors)
            
            lst=[]
            for i,column in enumerate(similarities.T):
                lst.append(sum(column)/len(data.iat[i,4].split(",")))
            
            data.insert(6,"similarities",lst,True)
            
            data=data.sort_values(by=["similarities"],ascending=False)
            
            #filtered_data = data[data['Needed_Exp'] <= user_exp]
            filtered_data = data[data['MIN_Needed_Exp'] <= user_exp]
            filtered_data=filtered_data[filtered_data['MAX_Needed_Exp']>=user_exp]
            
            filtered_data = filtered_data.sort_values(by=["similarities"], ascending=False)

            df1 = filtered_data.head(20)
            df2 = filtered_data.head(5)
            skills_list = df1['required_skills'].str.split(',').tolist()
            skills_list = [skill for sublist in skills_list for skill in sublist]
            remaining_skills = [skill for skill in skills_list if skill not in user_skills]
            skill_counts = Counter(remaining_skills)
            top_skills1 = [skill for skill, _ in skill_counts.most_common(4)]
            #print(top_skills1)
            df2['required_skills'] = df2['required_skills'].apply(lambda x: x.split(','))
            print(df2[["job_post","company","required_skills","job_location",'MIN_Needed_Exp','MAX_Needed_Exp',"similarities"]])
            response_data = df2[["job_post","company","job_description","required_skills", "job_location", "MIN_Needed_Exp", "MAX_Needed_Exp"]].to_dict(orient='records')

        #     jobs = data['Job Title']
        #     skills = data['Key Skills'].apply(lambda x: str(x)) # Convert to string
        #     #data.drop(data.columns[[1]], axis=1, inplace=True)
        #     vectorizer = TfidfVectorizer()
        #     skill_vectors = vectorizer.fit_transform(skills)
        #     user_vector = vectorizer.transform(user_skills)
        #     similarities = cosine_similarity(user_vector, skill_vectors)
        #     lst=[]
        #     for i,column in enumerate(similarities.T):
        #         #if isinstance(data.iat[i, 1], str):
        #         lst.append(sum(column)/len(data.iat[i,1].split("|")))
        #         #else:
        # # Handle non-string values (e.g., assign 0 or another value)
        #             #lst.append(0)  # Assuming 0 similarity for non-strings    
        #     #print(*lst)
        #     data.insert(10,"similarities",lst,True)
        #     data=data.sort_values(by=["similarities"],ascending=False)
        #     filtered_data = data[data['Needed_Exp'] <= user_exp]
        #     #df1=data.head(5)
        #     filtered_data = filtered_data.sort_values(by=["similarities"], ascending=False)
        #     df1 = filtered_data.head(5)
        #     print(df1[["Job Title","sal","Location","similarities","Needed_Exp"]])

            #ALGORITHM LOGIC ENDS 

            
            return Response({'data': response_data,"top_skills": top_skills1}, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = f"Error processing CSV file: {str(e)}"
            print(error_msg)
            print(i)# Print the error message
            return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class FindAlgorithmView(APIView):
    renderer_classes = [UserRenderer]  
    permission_classes = [IsAuthenticated]  
        # Parse JSON data from the request body
    def post(self, request, format=None):
        serializer = AlgorithmInputSerializer(data=request.data)
        if serializer.is_valid():
            skills11 = serializer.data.get('skill')
            split_string = [word.strip() for word in skills11.split(",")]
            skills1 = ",".join(split_string)
            print(skills1)
            user_exp = serializer.validated_data.get('yoe')
            original_skills = skills1.split(',')
            user_skills = [item.upper() for item in original_skills]
            print(user_skills)
    
        print(user_exp)
        print(user_skills)
        # Read the CSV file
        csv_file_path = "./account/dataset/jobss.csv"
       
        try:
          
            data = pd.read_csv(csv_file_path, encoding="utf8")
            if data is None:
                raise ValueError("Failed to load CSV data")

            # Explicitly replace NaN values with an empty string
            data['required_skills'] = data['required_skills'].fillna('')        
            # ALGORITHM LOGIC STARTS
            jobs = data['job_post']        
            skills = data['required_skills']
            #print(jobs)         
            data['required_skills'] = data['required_skills'].str.upper()       
            data.drop(data.columns[[0]],axis=1 ,inplace=True)        
            #data['Needed_Exp'] = data['Needed_Exp'].astype(int)        
            #data['Needed_Exp'].unique().astype(int)
            vectorizer=TfidfVectorizer()                     
            skill_vectors=vectorizer.fit_transform(skills)  
            for i in range(len(user_skills)):
                if user_skills[i] == "C":
                    user_skills[i] = "C LANGUAGE"
                elif user_skills[i] == "C++":
                    user_skills[i] = "CPP"
                elif user_skills[i]=="R":
                    user_skills[i]="MATLAB"
                elif user_skills[i]=="C#":
                    user_skills[i]="C HAS" 
                elif user_skills[i]=="CORE JAVA":
                    user_skills[i]="JAVA"
                elif user_skills[i]=="NODE.JS":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="NODE JS":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="NODE":
                    user_skills[i]="NODEJS"
                elif user_skills[i]=="REACT.JS":
                    user_skills[i]="REACTJS"
                elif user_skills[i]=="REACT JS":
                    user_skills[i]="REACTJS"
                elif user_skills[i]=="REACT":
                    user_skills[i]="REACTJS"            
        
            user_vector = vectorizer.transform(user_skills)           
            type(user_skills)           
            similarities = cosine_similarity(user_vector, skill_vectors)            
            lst=[]
            for i,column in enumerate(similarities.T):
                lst.append(sum(column)/len(data.iat[i,4].split(",")))            
            data.insert(6,"similarities",lst,True)            
            data=data.sort_values(by=["similarities"],ascending=False)            
            #filtered_data = data[data['Needed_Exp'] <= user_exp]
            filtered_data = data[data['MIN_Needed_Exp'] <= user_exp]
            filtered_data=filtered_data[filtered_data['MAX_Needed_Exp']>=user_exp]            
            filtered_data = filtered_data.sort_values(by=["similarities"], ascending=False)            
            df1 = filtered_data.head(20)
            df2 = filtered_data.head(5)
            # skills_list = df1['required_skills'].str.split(',').tolist()
            # skills_list = [skill for sublist in skills_list for skill in sublist]
            # remaining_skills = [skill for skill in skills_list if skill not in user_skills]
            # print(remaining_skills)
            # skill_counts = Counter(remaining_skills)
            # top_skills1 = [skill for skill, _ in skill_counts.most_common(4)]
            skills_list = df1['required_skills'].str.split(',').tolist()
            skills_list = [skill for sublist in skills_list for skill in sublist]
            #skills_list
            # Convert skills lists to sets for faster comparison
            # skills_set = set(skills_list)
            # user_skills_set = set(user_skills)

            # # Find the remaining skills by calculating the set difference
            # remaining_skills_set = skills_set - user_skills_set

            # # Convert the remaining skills set back to a list
            # remaining_skills = list(remaining_skills_set)
            # print(remaining_skills)    
            
            
            
            remaining_skills = [skill for skill in skills_list if skill not in user_skills]
            remaining_skills
            #from collections import Counter
            skill_counts = Counter(remaining_skills)
            top_skills1 = [skill for skill, _ in skill_counts.most_common(4)]
            print(top_skills1)
                    
            df2['required_skills'] = df2['required_skills'].apply(lambda x: x.split(','))
            
            print(df2[["job_post","company","required_skills","job_location",'MIN_Needed_Exp','MAX_Needed_Exp',"similarities"]])
            response_data = df2[["job_post","company","job_description","required_skills", "job_location", "MIN_Needed_Exp", "MAX_Needed_Exp"]].to_dict(orient='records')
            
            
            return Response({'data': response_data,"top_skills": top_skills1}, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = f"Error processing CSV file: {str(e)}"
            print(error_msg)
            print(i)# Print the error message
            return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        

class UserProfileUpdateView(APIView):
    renderer_classes = [UserRenderer]  
    permission_classes = [IsAuthenticated]  

    def patch(self, request, format=None):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       