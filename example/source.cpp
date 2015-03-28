#include "header.h"


//Test ignored comment


namespace Foo { namespace Bar { namespace Baz {


class MyType {};

MyType func(MyType const& param); //Not overqualified

Baz::MyType func(Baz::MyType const& param); //Overqualified
Bar::Baz::MyType func(Bar::Baz::MyType const& param); //Overqualified
Foo::Bar::Baz::MyType func(Foo::Bar::Baz::MyType const& param); //Overqualified


}}}


int main(int argc, char* argv[]) {
	return 0;
}

/*Test no concluding newline; C-style comment for CPIP's benefit*/