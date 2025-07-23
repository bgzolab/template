union semum{
    int val;
};
void sem_init(const int semid, const int num, const int val);
void sem_p(const int semid, const int num);
void sem_v(const int semid, const int num);
