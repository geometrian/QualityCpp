#include "header.h"


static int a;
/*Test ignored C comment*/
static int b;
/*Test ignored
multi-line
C comment*/
static int c;
//Test ignored C++ comment
static int d;


namespace Foo { namespace Bar { namespace Baz {


//Test stack-based preprocessor
#if 1
	#if 1
		namespace A {
			class MyType0 {};
			A::MyType0 overqualified0;
	#else
		namespace B {
	#endif
			A::MyType0 overqualified1;
			static int e;
		}
#else
	static int f;
#endif


class MyType {};

MyType not_overqualified

Baz::MyType overqualified2;
Bar::Baz::MyType overqualified3;
Foo::Bar::Baz::MyType overqualified4;


}}}


int main(int argc, char* argv[]) {
	return 0;
}


//Test no concluding newline