#include <iostream>
#include <string>

using namespace std;


int main()
{
	string s;
	getline(cin,s);

	int i=0,depth=0;
	while(i < s.size())
	{
		if(s[i]=='('||s[i]=='['||s[i]=='{')
		{
			cout<<s[i];
			cout<<endl;
			depth++;
			for(int j=0;j<depth;j++)
				cout<<"\t";
		}
		else if(s[i]==')'||s[i]==']'||s[i]=='}')
		{
			cout<<endl;
			depth--;
			for(int j=0;j<depth;j++)
				cout<<"\t";
			cout<<s[i];
			cout<<endl;
			for(int j=0;j<depth;j++)
				cout<<"\t";
		}
		else if(s[i]==',')
		{
			cout<<s[i];
			cout<<endl;
			for(int j=0;j<depth;j++)
				cout<<"\t";
			if(s[i+1]==' ')
				i++;
		}
		else
		{
			cout<<s[i];
		}
		i++;
	}

	return 0;
}
