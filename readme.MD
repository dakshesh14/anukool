# Anukool

An AI powered project to help job seekers by crafting cover letters. Host it on your local machine and use it to generate cover letters for your job applications.

![image](https://github.com/dakshesh14/anukool/assets/65905942/08ca8ec6-3b88-4ad8-927a-d70efd8d3b43)

## Setup

1. Clone the repo

```bash
git clone https://github.com/dakshesh14/anukool.git
cd anukool
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Add the environment variables and populate them

```bash
cp .env.example .env
```

5. Add your pdf in `docs` folder.

6. Run the script

```bash
uvicorn main:app --reload
```

7. Open the browser and go to `http://localhost:8000/` to view the app.

## Contributing

Contributions are welcome! In fact to promote the open source culture, I launched this project in under GPL-3.0 License. Feel free to open an issue or submit a pull request.

## Acknowledgements

- FastAPI
- LangChain
- OpenAI
- and others for their unwavering support.

## Future Scope

- [ ] Reduce hallucination
- [ ] Add option for llama-2 model
- [ ] Add option for users to get a resume generated for the same job
- [ ] Add option to get output for more commonly asked questions

## Conclusion

While this project is far from perfect, I wish that it will bring value to the community and the job seekers. I hope that it will help you in your job search. If you like this project, please consider giving it a star. If you want to connect with me, you can find me on the following platforms:

- [LinkedIn](https://www.linkedin.com/in/dakshesh-jain/)
- [Twitter](https://twitter.com/_dakshesh)
- [GitHub](https://github.com/dakshesh14)
- [Reddit](https://www.reddit.com/user/_dakshesh/)
