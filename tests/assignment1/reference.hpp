
template <class T>
class stack {

    public:

        stack(int size) {
            data = new T[size];
            max = size;
        }

        stack() {
            data = new T[50];
            max = 50;
        }

        bool push(T item) {
            if(this->size < max) {
                data[this->size++] = item;
                return true;
            } else {
                return false;
            }
        }

        T pop() {
            if(this->size > 0) {
                return data[--this->size];
            } else {
                return 0;
            }
        }

        bool isEmpty() {
            return (this->size == 0) ? true : false;
        }

        bool isFull() {
            return (this->size == max) ? true : false;
        }

    private:

        T* data;
        int size = 0;
        int max = -1;

};

