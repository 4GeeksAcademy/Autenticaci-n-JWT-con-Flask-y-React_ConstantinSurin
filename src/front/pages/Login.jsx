import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (!email || !password) {
            setError("Todos los campos son requeridos");
            return;
        }

        try {
            const backendUrl = import.meta.env.VITE_BACKEND_URL;
            const res = await fetch(`${backendUrl}api/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();

            if (res.ok) {
                sessionStorage.setItem("token", data.token);
                navigate("/profile");
            } else {
                setError(data.msg || "Error al iniciar sesión");
            }
        } catch {
            setError("Error de conexión con el servidor");
        }
    };

    return (
        <div style={{ width: "300px", margin: "50px auto", textAlign: "center" }}>
            <h2>Inicio de sesión</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{ display: "block", width: "100%", marginBottom: "10px" }}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ display: "block", width: "100%", marginBottom: "10px" }}
                />
                {error && <p style={{ color: "red" }}>{error}</p>}
                <button type="submit">Entrar</button>
            </form>
        </div>
    );
}
