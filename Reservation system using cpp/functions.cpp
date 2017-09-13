#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<iomanip>
using namespace std ;
string busbase = "/home/mani/Documents/c++/Bus Resevation System/bus" ;// change the path
void bus_display() ;

int payment ( int , int ) ;
int check ( int ,int ) ;
string cancel_buspath(int) ;
typedef struct  bus_details
  {
    string buspath ;
    int bus_num ;
  } rec ;
rec bus_select();
void booking ( string str )
 {
   rec recieve ;
   recieve = bus_select() ;
   const char *   path = recieve.buspath.c_str() ;
   ifstream iseats ;
   iseats.open(path) ;
   int s[30] ;
   string name[30];
   int b = 0 ;
   int c ;
   string ss ; 
   while( getline ( iseats , ss ) )
    {
      istringstream split1(ss) ;
      split1 >> s[ b ] ;
      split1 >> name[b] ;
      b++ ;
    }
   iseats.close();
   for( int i = 0 ; i < 30 ; i++ )
   {
   cout.width(2) ;
   cout<<i+1;
   cout<<"    ";
   if( s[i] == 1 )
    {
     cout<<" Booked "<<endl;
    }
   else if( s[i] == 0 )
    {
     cout<<" Vacant "<<endl;
    }
   else
    {
       cout<<" something went wrong "<<endl;
       return ;
    } 
   } 
   cout<<" select your desired seat : "<<endl;
   select :
   cin>>c ;
      if( s[c-1] != 0 || ( c > 30 ) || ( c < 1 )  ) // availability check
       {
         cout<<"seat not available "<<endl;
         goto select ;
       }
    else
      {
       int k = payment( c , recieve.bus_num ) ;
       if(k == 1)
        {
       s[c-1] = 1 ;
       name[c-1] = str ;
       cout<<"         MSRIT      "<<endl;
       cout<<" Name : "<<str<<endl;
       cout<<" Bus number : "<<recieve.bus_num<<endl;
       cout<<" Seat number : "<<c<<endl;
        }
       else
        {
          cout<<" Transaction failed "<<endl ;
        }
      }
   ofstream fseats  ;
   fseats.open(path) ;
   for(int i = 0 ; i < 30  ; i++ )
    {
     fseats<<s[i]<<" "<<name[i]<<endl;
    }
   fseats.close();

 }
void cancel( string str ) 
 {
   
   int a1 ;
   cout<<" Please enter your transaction id : "<<endl;
   cin>>a1 ;
   int r ;
   r = a1 % 19200498 ;
   int r1 = (a1-r) / 19200498 ;
   string recieve ;
   recieve = cancel_buspath(r) ;
   const char * path = recieve.c_str() ;
   ifstream Iseats ;
   Iseats.open(path) ;
   int s1[30] ;
   string name1[30] ;
   int b1 = 0 ;
   string ss1 ; 
   while( getline( Iseats , ss1 ) )
    {
      istringstream split2(ss1) ;
      split2>>s1[b1] ;
      split2>>name1[b1] ;
      b1++ ;
    }
   Iseats.close();

   if( s1[r1-1] == 1 && name1[r1-1] == str )
    {
   cout<<" You have booked a ticket corresponding to seat number : "<<r1<<" in bus number : "<<r<<endl;
   cout<<" Would like to cancel it (Y/N) : "<<endl;
   char t ;
   cin>>t ;
   switch (toupper(t))
     {
       case ('Y' ) :
         {
          s1[r1-1] = 0;
          name1[r1-1] = "NONE" ;
          cout<<" you have canceled the ticket : "<<r1<<endl;
          break;
         }
       case ('N' ) :
         {
          cout<<" Looks like you have lost your way . "<<endl;
          return ;
          break;
         }
       default :
         {
           cout<<" Invalid input "<<endl;
         }
      }
    }
   else
    {
     cout<<" Invalid transaction id  "<<endl;
    }       
   ofstream Fseats  ;
   Fseats.open(path) ;
   for(int i = 0 ; i < 30  ; i++ )
    {
     Fseats<<s1[i]<<" "<<name1[i]<<endl;
    }
   Fseats.close(); 
 } 

int payment(int a ,int b )
  {
    
    cout<<" Please complete the transaction procedure to complete the booking procedure : "<<endl;
    cout<<" An amount of Rs. 150.00 will be debited to your account . "<<endl;
    string cardholder ;
    long long int cardnumber ;
    int cvv , month , year ;
    cout<<" Enter the card holder name : "<<endl;
    getline(cin, cardholder);
    getline(cin, cardholder);
    cout<<" Enter the card number : "<<endl;
    cin>>cardnumber ;
    retake1 :
    cout<<" Enter the expiry date ( MM YYYY ) : "<<endl;
    cin>>month>>year;
    if( ( month < 1 ) || (month > 12 ) )
     {
        cout<<" Invalid  month . "<<endl;
        goto retake1 ;
      }
    cout<<" Enter the CVV : "<<endl;
    cin>>cvv ;
    cout<<" Please press 1 to confirm the transaction . "<<endl;
    int k2 ;
    cin>>k2;
    if( k2 == 1 )
     { 
    int k1 ;
    k1 = check( month , year ) ;
    if( k1  == 1 )
     {
    long long int tid ; 
    tid = 19200498 * a + b ; // generating an unique  transaction id
    cout<<" Your transaction id is : "<<tid<<endl;
    cout<<" Please retain your transaction id for further assistance . "<<endl;   
    return 1 ;
     }
    else
     {
       return 0 ;
     }
     }
    else
     {
       cout<<" You have canceled the payment . "<<endl;
       return 0 ;
     }
  }

int check (int a ,int b ) // validating the card expiry date .
 {
   // current date/time based on current system
   time_t now = time(0);

   tm *current = localtime(&now);
   
   if( ( b > ( 1900 + current->tm_year ) ) || ( ( b == ( 1900 + current->tm_year ) ) && ( a > ( 1 + current->tm_mon ) ) ) )
    {
      return 1 ;
    }
   else
    {
      return 0;
    }
 }
 
void welcome()
  {
    cout<<"# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # "<<endl;
    cout<<" # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #"<<endl;
    cout<<"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;
    cout<<"                              WELCOME TO MSRIT                                "<<endl;
    cout<<"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;
  }

void  welcome_note()
  {
    cout<<"##############################################################################"<<endl;
    cout<<"#################################          ###################################"<<endl;
    cout<<"################################     M      ##################################"<<endl;
    cout<<"###############################      S       #################################"<<endl;
    cout<<"##############################       R        ################################"<<endl;
    cout<<"###############################      I       #################################"<<endl;
    cout<<"################################     T      ##################################"<<endl;
    cout<<"#################################          ###################################"<<endl;
    cout<<"##############################################################################"<<endl;
  }

void bus_seats()
  {
    cout<<" The seating of the  bus is as shown below : "<<endl<<endl;
    cout<<"------------------------------------- "<<endl;
    cout<<"|    30  29                28  27   | "<<endl;
    cout<<"|    26  25                24  23   | "<<endl;
    cout<<"|    22  21                20  19   | "<<endl;
    cout<<"|    18  17                16  15   | "<<endl;
    cout<<"|    14  13                12  11   | "<<endl;
    cout<<"|    10  09                08  07   | "<<endl;
    cout<<"|    06  05                04  03   | "<<endl;
    cout<<"|    02  01                conductor| "<<endl;
    cout<<"|                                  D  "<<endl;
    cout<<"|                                  O  "<<endl;
    cout<<"|                                  O  "<<endl;
    cout<<"|                                  R  "<<endl;
    cout<<"|  Driver                           | "<<endl;
    cout<<"------------------------------------- "<<endl;
  }

rec bus_select()
  {
    bus_display() ;
    cout<<"Select your bus : "<<endl;
    int choice ;
    cin>>choice  ;
    struct bus_details result ;
    bus_seats() ;
    switch(choice) 
      {
        case(1)  :
         {
           result.buspath = busbase + "1.txt" ;
           result.bus_num = 1 ;
           return result ;
           break ;
         }
        case(2) :
         {
           result.buspath = busbase + "2.txt" ;
           result.bus_num = 2 ;
           return result ;
           break ;
         }
        default :
         {
           cout<<"Invalid Input . "<<endl;
           break ;
         }
      }
  }
 
void bus_display()
  {
    cout<<" Services available : "<<endl;
    cout<<" 1 : Bangalore Express "<<endl<<" 2 : Hyderabad Express "<<endl;
  }       

string cancel_buspath(int a)
  {
    string buspath ;
    switch ( a )
     {
       case(1) :
         {
           buspath = busbase + "1.txt" ;
           return buspath ;
           break  ;
         }
       case(2) :
         {
           buspath = busbase + "2.txt" ;
           return buspath ; 
           break;
         }
       default :
         {
           cout<<" Invalid Transaction id . "<<endl;
           break ;
         }
     }
  }
