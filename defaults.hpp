#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <functional>

#pragma once

using std::string;
using std::vector;
using std::function;

int toInt(string string){
	int i;

	std::istringstream(string) >> i;

	return i;
}

template<typename vtype>
class Array{
	vector<vtype> array;

	public:
		template<typename... Ts>
		Array(Ts... vals){
			vector<vtype> vs = {vals...};
	
			for(int i = 0; i < vs.size(); i++){
				array.push_back(vs[i]);
			}
		}

		Array(){}

		void append(vtype val){
			array.push_back(val);
		}

		template<typename... Ts>
		void append(Ts... vals){
			vector<vtype> vs = {vals...};

			for(int i = 0; i < vs.size(); i++){
				array.push_back(vs[i]);
			}
		}

		vtype get(int index) const {
			return array[index];
		}

		int length() const {
			return array.size();
		}

		void remove(int index){
			array.erase(array.begin() + index);
		}

		void clear(){
			array.clear();
		}

		void forEach(function<void(int,vtype)> f) const {
			for(int i = 0; i < array.size(); i++){
				f(i,array[i]);
			}
		}

		template<typename T>
		friend std::ostream &operator << (std::ostream &output,Array<T> &ar);
};

class COLORS_BOLD_CLASS{
	public:
		string BLACK = "\u001b[30;1m";
		string RED = "\u001b[31;1m";
		string GREEN = "\u001b[32;1m";
		string YELLOW = "\u001b[33;1m";
		string BLUE = "\u001b[34;1m";
		string MAGENTA = "\u001b[35;1m";
		string CYAN = "\u001b[36;1m";
		string WHITE = "\u001b[37;1m";
};

class COLORS_CLASS{
	public:
		string BLACK = "\u001b[30m";
		string RED = "\u001b[31m";
		string GREEN = "\u001b[32m";
		string YELLOW = "\u001b[33m";
		string BLUE = "\u001b[34m";
		string MAGENTA = "\u001b[35m";
		string CYAN = "\u001b[36m";
		string WHITE = "\u001b[37m";
		string RESET = "\u001b[0m";

		COLORS_BOLD_CLASS BOLD;
};

class TORONTO_CLASS{
	public:
		COLORS_CLASS COLORS;

		template<typename T>
		void print(T val){
			std::cout << val;
		}

		template<typename T>
		void printl(T val){
			std::cout << val << std::endl;
		}

		void endl(){
			std::cout << std::endl;
		}

		string input(string prompt){
			string input;
			
			std::cout << prompt;
			std::cin >> input;

			return input;
		}
};

TORONTO_CLASS TORONTO;

template<typename T>
std::ostream &operator << (std::ostream &output,Array<T> &ar){
	string message = "[ ";
	
	for(int i = 0; i < ar.length(); i++){
		if(std::is_same<T,string>::value){
			message += "\"";
			message += ar.get(i);
			message += "\"";
		} else{
			std::stringstream s;
			s << ar.get(i);
			
			message += s.str();
		}

		if(!(i >= ar.length() - 1)) message += ", ";
	}
	
	message += " ]";

	output << message;
		
	return output;
};