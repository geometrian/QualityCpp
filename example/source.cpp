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


namespace Foo { namespace Bar {
	namespace _Baz {
		class ConfusingUnderline;
	}
namespace Baz {


//Test stack-based preprocessor
#if 1
	#if 1
		namespace A {
			class MyType0 { int my_type0; }; //Test no final
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


//Test no final
class Okay1 final { //okay
	~Okay1(void) = default;
};
class Okay2 { //okay
	virtual ~Okay2(void) = default;
};
class Bad1 final { //bad; shouldn't have both final and virtual
	virtual ~Bad1(void) = default;
};
class Bad2 { //bad; shouldn't have neither final nor virtual
	~Bad2(void) = default;
};
template <typename Channel, int bitsR> class Bad3 { public: Channel r:bitsR; }; //bad; template class shouldn't have neither final nor virtual
template <> class Bad3<float16_t,16> { public: float16_t r; }; //bad; template class shouldn't have neither final nor virtual
template <> class Bad3<    float,32> { public:     float r; }; //bad; template class shouldn't have neither final nor virtual
template <typename Channel, int bitsR> class Bad4 : public virtual Parent<bitsR> { //bad; template class shouldn't have neither final nor virtual
	public: Channel r:bitsR;
};


//Test overqualification
Okay1 not_overqualified;
_Baz::ConfusingUnderline not_overqualified2;
Baz::Okay1 overqualified2;
Bar::Baz::Okay1 overqualified3;
Foo::Bar::Baz::Okay1 overqualified4;


}}}


int main(int argc, char* argv[]) {
	return 0;
}


//Test no concluding newline