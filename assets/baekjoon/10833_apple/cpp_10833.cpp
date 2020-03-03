#include <iostream>
using namespace std;

int main(void)
{
    ios_base ::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
    int num;
    cin >> num;

    int a;
    int b;
    int ans = 0;

    for (int i = 0; i < num; i++)
    {
        cin >> a >> b;
        ans += b % a;
    }
    cout << ans << "\n";
    //system("pause");
    return 0;
}
