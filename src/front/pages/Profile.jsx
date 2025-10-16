import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Profile() {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        const backendUrl = import.meta.env.VITE_BACKEND_URL;

        fetch(`${backendUrl}api/profile`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
            .then(async (res) => {
                if (!res.ok) {
                    throw new Error("No autorizado");
                }
                const data = await res.json();
                setMessage(data.msg);
            })
            .catch(() => {
                sessionStorage.removeItem("token");
                navigate("/login");
            });
    }, [navigate]);

    return (
        <div style={{ width: "400px", margin: "50px auto", textAlign: "center" }}>
            <h2>Página Privada</h2>
            <p>{message}</p>
            <iframe
                width="600"
                height="400"
                src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&controls=1&loop=1&playlist=dQw4w9WgXcQ"
                title="Never Gonna Give You Up"
                frameBorder="0"
                allow="autoplay; encrypted-media"
                allowFullScreen
            ></iframe>
        </div>
    );
}
