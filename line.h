#include"dot.h"

class line{
	double k;
	double b;
public:
	line();
	line(dot, dot);

	bool is_dot_existed(line) const;
	dot get_dot_with_line(line) const;

	double get_k() const;
	double get_b() const;

};
