#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<unistd.h>
#include<iomanip>
#include"/home/mani/Documents/c++/Bus Resevation System/functions.cpp" // change the path
using namespace std;
int i , j = 0 ; // i = number of users registerd 
int user(string);  // getting the index of the user
int pass(int , string ); // password authentication
int reg();  // registering users
void booking(string); // booking a ticket
void cancel(string) ; // canceling a ticket
int payment(int , int) ; // payment gateway
int check(int , int ) ; // checking card's expiry date
void welcome() ; 
void welcome_note() ;
void bus_seats() ;
void geti() ; // getting number of users from text file
void puti() ; // writing updated number of users to the text file
void getusers() ; // getting users from text file
void putusers()  ; // updating users to text file
rec bus_select(); //  selection of bus
void bus_display() ; 
string users[100] ; 
string pwd[100] ;
int main()
 {

   geti() ;
   getusers() ;
   welcome() ;
   login :
   cout<<" 1: login 2 : register 3 : exit"<<endl;
   int z;
   cin>>z;
   switch(z)
    {
     case (1):
     { 
   string un,p;
   cout<<" Enter your username :  ";
   cin>>un;   
   p = getpass(" Enter password : ") ;
   int a;
   a = user(un) ;
   int key;
   key = pass( a , p ) ;
   if ( key == 1 )
    {
     cout<<" Welcome "<<un<<endl;
     welcome_note();
  int choice ;
  functions :
  cout<<" 1 : Book a ticket "<<"  2 : Cancel a ticket "<<" 3 : exit "<<endl;
  cin>>choice;
  switch(choice)
   {
    case 1 :
       {
         bus_seats() ;
         booking(un);
         goto functions ;
         break;
       }
     case 2 :
       {
        cancel(un);
        goto functions ;
        break;
        }
    case 3 :
        {
          return 0 ;
          break ;
        } 
   default :
        cout<<" Invalid Input "<<endl;
        break;
   }
    }
   else
    {

     cout<<" Invalid credentials "<<endl;
     
    }
     break;
      } 
      case (2):
       { 
       int g ;
        g = reg();

       
        if( g == 1 )
         {
          goto login ;
         }
        else
         {
          cout<<" Something has gone wrong . "<<endl;
         }
        break;
        }
      case  (3) :
        {
          return 0 ;
          break  ;
        }
     default :
      cout<<"  Invalid "<<endl;
      break;
     }
  return 0;
 }

int user(string a)
 {
  for(int i = 0 ; i<100 ; i++ )
   {
     if( a == users[i] )
      {
        return i ;
        break ;
      }

   }
    
        cout<<" user not found "<<endl;
        return -1;
 }
int pass(int i , string pw)
  {
     if( pw == pwd[i] )
      {
        return 1;
      }
     else
      {
        return 0 ;
      }
  }
int reg()
 {
   geti() ;
   cout<<i<<endl;
   int counter = 1 ;
   string tmpun ;
  while ( counter == 1 )
   {
  cout<<" Enter your  desired id : "<<endl;
  //string tmpun ;
  cin>>tmpun ;
  int flag = 0 ;
  for(int n =0 ; n<i ; n++ )
   {
    if( tmpun == users[n] )
     {
       flag = 1 ;
       break ;
      }
     else 
      {
        //flag does not change
      }
    }
   if( flag == 1 )
      {
        cout<<" ID not available ." <<endl;
      }
   else 
      {
        users[i] = tmpun ;
        counter = 0 ;
      }
   }
   pwd[i] = getpass(" Enter your  password : ") ;
   i++ ;
   puti() ;
   putusers() ;
   return 1 ;
 }  
 
void geti()
  {
   ifstream myfile ;
   myfile.open("/home/mani/Documents/c++/Bus Resevation System/i.txt") ; // change the path
   myfile>>i;
   
   myfile.close();
  }
void puti()
  {
   ofstream my ;
   my.open("/home/mani/Documents/c++/Bus Resevation System/i.txt") ; //change the path
   my << i;
   my.close();
   
  }

void getusers()
 {
   string s ;
   ifstream userss ;
   userss.open("/home/mani/Documents/c++/Bus Resevation System/users.txt" , ios :: in ) ; //change the path
  
   

   

   while( getline ( userss , s ) ) 
    {
     istringstream split( s ) ;
     split >> users[j] ;
     split >> pwd[j] ;

     j++ ;       
    }

   userss.close() ;
 }

void putusers()
 {
   ofstream file ;
   file.open("/home/mani/Documents/c++/Bus Resevation System/users.txt" ,ios::app) ; //change the path
   file<<users[i-1]<<" "<<pwd[i-1]<<endl;
   file.close();
 }
