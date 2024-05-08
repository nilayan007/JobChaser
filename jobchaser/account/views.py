from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer , UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer,AlgorithmViewSerializer
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
            return Response({'errors':{'non_field_errors':['email or password is not valid ']}},status = status.HTTP_404_NOT_FOUND)
        
    
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
    
       
        skills1 = serializer.data.get('skills')
        user_exp = serializer.data.get('year_of_experience')
        original_skills = skills1.split(',')
        user_skills =  [item.upper() for item in original_skills]
        print(user_exp)
        print(user_skills)
        # Read the CSV file
        csv_file_path = "./account/dataset/jobss.csv"
       
        try:            
            data = pd.read_csv(csv_file_path, encoding="utf8")
            
            # Extract job titles and key skills
            
            
            
            # ALGORITHM LOGIC STARTS
            jobs = data['Job Title']
            skills = data['Key Skills'].apply(lambda x: str(x)) # Convert to string
            #data.drop(data.columns[[1]], axis=1, inplace=True)
            vectorizer = TfidfVectorizer()
            skill_vectors = vectorizer.fit_transform(skills)
            user_vector = vectorizer.transform(user_skills)
            similarities = cosine_similarity(user_vector, skill_vectors)
            lst=[]
            for i,column in enumerate(similarities.T):
                #if isinstance(data.iat[i, 1], str):
                lst.append(sum(column)/len(data.iat[i,1].split("|")))
                #else:
        # Handle non-string values (e.g., assign 0 or another value)
                    #lst.append(0)  # Assuming 0 similarity for non-strings    
            #print(*lst)
            data.insert(10,"similarities",lst,True)
            data=data.sort_values(by=["similarities"],ascending=False)
            filtered_data = data[data['Needed_Exp'] <= user_exp]
            #df1=data.head(5)
            filtered_data = filtered_data.sort_values(by=["similarities"], ascending=False)
            df1 = filtered_data.head(5)
            print(df1[["Job Title","sal","Location","similarities","Needed_Exp"]])

            #ALGORITHM LOGIC ENDS 
            
            
            
            return Response({'msg': 'output loaded successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            error_msg = f"Error processing CSV file: {str(e)}"
            print(error_msg)  # Print the error message
            return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)