{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "03ef1658-b123-43b1-a3d1-894aa3683375",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'testadd'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-6-dfd48ecd0c92>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mtestadd\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0madd\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'testadd'"
     ]
    }
   ],
   "source": [
    "from testadd import add"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5599b88e-da71-4ceb-9cb2-1905ce24810b",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "d103a95c-7024-4e2a-a5f8-830d20ac80d5",
   "metadata": {},
   "outputs": [],
   "source": [
    "def func(a: 'spam', b: (1, 10), c: float) -> int:\n",
    "    return a + b + c\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "e23e58ea-962e-42db-ba10-f196fe9f7d07",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'a': 'spam', 'b': (1, 10), 'c': float, 'return': int}"
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "func.__annotations__"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ea4670b3-99af-4dde-8c72-28f94de329b1",
   "metadata": {},
   "outputs": [],
   "source": [
    "func.__annotations__"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6645eee8-4bee-4c0e-8e4e-fb75cd7f2725",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "import sys \n",
    "from tkinter import Button, mainloop # Tkinter in 2.X \n",
    "x = Button(text='Press me', command=(lambda:sys.stdout.write('Spam\\n'))) # 3.X: \n",
    "print() \n",
    "x.pack() \n",
    "mainloop() "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9c34dca7-cf27-463d-bc6d-12ceae6941ed",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
