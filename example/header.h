#pragma once

//Test header


//Good; should not be caught by final/virtual rule.
enum class MyEnum {
	POMEGRANATE
};

class FooClass final {
	virtual void method(void) const = 0;
};

class BarClass final : public FooClass {
	virtual ~BarClass(void) {} //Bad; should be "default"ed

	//Bad; should have been tagged "virtual"
	void method(void) const override {}
};
