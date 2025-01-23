document.getElementById("login-form").addEventListener("submit", async function (event) {
  event.preventDefault(); // Предотвращаем перезагрузку страницы

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorMessage = document.getElementById("error-message");

  try {
    // Отправляем запрос к вашему бэкенду
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      alert(`Login successful! Your token is: ${data.access_token}`);
      errorMessage.textContent = ""; // Очищаем ошибку
    } else {
      const errorData = await response.json();
      errorMessage.textContent = errorData.detail || "Login failed. Please try again.";
    }
  } catch (error) {
    console.error("Error during login:", error);
    errorMessage.textContent = "An error occurred. Please try again later.";
  }
});