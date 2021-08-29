from bs4 import BeautifulSoup
import requests
from flask import Flask, redirect, url_for, request, render_template
import os
import random



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# modify the input to convert spaces to '+' to put it in the URL


def modifyInput(input):
    afterChange = input.replace(" ", "+")
    return afterChange


info = []


def getCompanyName(jobTitle, link, number):
    request = requests.get(link)
    plainText = request.text
    soup = BeautifulSoup(plainText, "html.parser")
    for companyName in soup.findAll(
        "div", {"class": "icl-u-lg-mr--sm icl-u-xs-mr--xs"}
    ):

        textInfo = soup.find("div", {"class": "jobsearch-jobDescriptionText"})
        user = {}

        if companyName.text != "-":
            jobTitleAfterReplaced = jobTitle.replace("\n", "")
            user["jobTitle"] = jobTitleAfterReplaced
            user["company"] = companyName.text
            user["link"] = link
            user["information"] = textInfo.text
            target = generate_id()
            user['dataTarget'] = target
            user['targetId'] = target.replace('#', '')
            # number = generateNumbers(number)
            user['index'] = number

            info.append(user)

        return info


num = 2


def generate_id():
    num = random.randrange(0, 1000)
    id = "#demo" + str(num)
    return id


@app.route("/", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        searchResult = request.form["search"]
        numOfPages = int(request.form['pages'])

        startPage = 1
        number = 1
        while startPage <= numOfPages:
            jobAfterEdit = modifyInput(searchResult)
            # print(jobAfterEdit)
            url = f"https://www.indeed.com/jobs?q={jobAfterEdit}&start=" + str(
                startPage * 10
            )
            sourceCode = requests.get(url)
            plainText = sourceCode.text
            soup = BeautifulSoup(plainText, "html.parser")
            startPage += 1
            for divs in soup.findAll("a", {"class": "jobtitle turnstileLink"}):
                href = "https://www.indeed.com" + divs.get("href")
                jobTitle = divs.text
                link = href
                data = getCompanyName(jobTitle, link, number=number)
                lengthOfResults = len(info)
                number += 1
        return render_template("home.html", data=data, lengthOfResults=lengthOfResults)

    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
