#include<iostream>
using namespace std;
int main(){
    // From IMUDGESOJ -RID:96804 -PID:1316 -RES:4 -LANG:1
    int N, j;
    cin >> N;
    if (N < 3){
        if (N < 0) return 0;
        if (N == 0)cout << "0";
        if (N == 1)cout << "1";
        if (N == 2)cout << "1";
    }
    else{
        N -= 2;
        int a[5000] = { 0 }, b[5000] = { 0 }, c[5000] = { 0 };
        a[0] = 1;
        b[0] = 1;
        for (int i = 0; i < N; i++){
            for (j = 0; j < N; j++){
                c[j] += a[j] + b[j];
                if (c[j] > 9){
                    c[j] -= 10;
                    c[j + 1] = 1;
                }
            }
            swap(a, b);
            swap(b, c);
            for (int i = 0; i < 5000; i++) c[i] = 0;
        }
        for (j; b[j] == 0; j--);
        for (j; j >= 0; j--)cout << b[j];
    }
}