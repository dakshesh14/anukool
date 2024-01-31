const myForm = document.getElementById("myForm");
const userInfoForm = document.getElementById("userInfoForm");
const generateButton = document.getElementById("generateButton");
const copyButton = document.getElementById("copyButton");
const downloadAsPDFButton = document.getElementById("downloadButton");
const contentArea = document.getElementById("contentArea");

const myGenerationOutputModal = new bootstrap.Modal(
  document.getElementById("coverLetterOutput")
);

const myGetUserInfoModal = new bootstrap.Modal(
  document.getElementById("getUserInfoModal")
);

const generateAndDownloadPDF = (data) => {
  axios({
    method: "POST",
    url: "/generate-pdf",
    data: data,
  }).then((res) => {
    const blob = new Blob([res.data], { type: "application/pdf" });

    const link = document.createElement("a");
    link.href = window.URL.createObjectURL(blob);
    link.download = "cover_letter.pdf";
    link.click();
  });
};

myForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(myForm);

  const aboutJob = formData.get("aboutJob");
  const aboutCompany = formData.get("aboutCompany");

  const payload = {
    job_description: aboutJob,
    company_description: aboutCompany,
  };

  generateButton.setAttribute("disabled", "disabled");
  generateButton.innerText = "Generating...";

  axios({
    url: "/chat",
    method: "POST",
    data: payload,
  })
    .then((res) => {
      const modalContentArea = document.getElementById("modalOutputArea");
      modalContentArea.innerText = res.data.answer;

      myGenerationOutputModal.show();
    })
    .catch((err) => {
      console.error(err);
    })
    .finally(() => {
      generateButton.removeAttribute("disabled");
      generateButton.innerText = "Generate";
    });
});

copyButton.addEventListener("click", (e) => {
  const modalContentArea = document.getElementById("modalOutputArea");
  const textToCopy = modalContentArea.innerText;

  navigator.clipboard.writeText(textToCopy);

  copyButton.innerText = "Copied!";

  const timeout = setTimeout(() => {
    copyButton.innerText = "Copy";
    clearTimeout(timeout);
  }, 2000);
});

downloadAsPDFButton.addEventListener("click", (e) => {
  // for some reason, the modal doesn't close when .hide() is called once
  myGenerationOutputModal.hide();
  myGenerationOutputModal.hide();

  myGetUserInfoModal.show();

  const userInfo = localStorage.getItem("userInfo");
  if (userInfo === null) return;

  document.getElementById("fullName").value = JSON.parse(userInfo).full_name;
  document.getElementById("jobTitle").value = JSON.parse(userInfo).job_title;
  document.getElementById("saveLocal").checked = true;
});

userInfoForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = new FormData(userInfoForm);

  const fullName = formData.get("fullName");
  const jobTitle = formData.get("jobTitle");
  const saveLocal = formData.get("saveLocal");

  const content = document.getElementById("modalOutputArea").innerText;

  const payload = {
    full_name: fullName,
    job_title: jobTitle,
    content,
  };

  if (saveLocal === "on")
    localStorage.setItem(
      "userInfo",
      JSON.stringify({
        full_name: fullName,
        job_title: jobTitle,
      })
    );

  generateAndDownloadPDF(payload);

  myGetUserInfoModal.hide();
});
