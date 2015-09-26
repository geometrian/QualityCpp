#pragma once

//Test header


class FooClass final {
	virtual void method(void) const = 0;
};
class BarClass final : public FooClass {
	virtual ~BarClass(void) {} //Bad; should be "default"ed

	//Bad; should have been tagged "virtual"
	void method(void) const override {}
};
