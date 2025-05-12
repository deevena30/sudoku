#include <bits/stdc++.h>
using namespace std;

void func(int n){
    // for(int i=1;i<n;i++){
    //     cout<<i<<endl;
    // }

    if(n<=0) return;
    cout<<n<<endl;
    func(n-1);
    cout<<n<<endl;
    

}

int main(){
    int n;
    cin>>n;
    func(n);
}