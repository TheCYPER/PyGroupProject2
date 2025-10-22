#include <iostream>
#include <string>
#include <random>
using namespace std;

const int MAXN = 1e7;

string GS(int length) {
    // Define the list of possible characters
    const string CHARACTERS
        = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv"
          "wxyz0123456789";

    // Create a random number generator
    random_device rd;
    mt19937 generator(rd());

    // Create a distribution to uniformly select from all
    // characters
    uniform_int_distribution<> distribution(
        0, CHARACTERS.size() - 1);

    // Generate the random string
    string random_string;
    for (int i = 0; i < length; ++i) {
        random_string
            += CHARACTERS[distribution(generator)];
    }

    return random_string;
}

int main () {
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    freopen("books.json", "w", stdout);
    cout << "[\n";
    for (int i = 1; i <= MAXN - 1; ++i) {
        cout << "{\n";
        cout << "\"title\": \"";
        cout << GS(5) << "\"\n";
        cout << "},\n";
    }
    cout << "{\n";
    cout << "\"title\": \"";
    cout << GS(5) << "\"\n";
    cout << "}\n";

    printf("]");
    return 0;
}
