{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1dea85fc-fd07-4117-b843-751e65a25d48",
   "metadata": {},
   "outputs": [],
   "source": [
    "class Univariate():\n",
    "    \n",
    "    def quanQual(dataset):\n",
    "        qual = []\n",
    "        quan = []    \n",
    "        for colName in dataset.columns:\n",
    "            if dataset[colName].dtype == \"O\":\n",
    "                qual.append(colName)\n",
    "            else:\n",
    "                quan.append(colName)\n",
    "    \n",
    "        return quan, qual"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
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
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
