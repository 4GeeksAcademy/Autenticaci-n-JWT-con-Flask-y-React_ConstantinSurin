// src/pages/Private.jsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Profile() {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        if (!token) {
            navigate("/login");
            return;
        }

        axios.get("http://localhost:5000/private", {
            headers: { Authorization: `Bearer ${token}` }
        }).then(res => {
            setMessage(res.data.msg);
        }).catch(err => {
            sessionStorage.removeItem("token");
            navigate("/login");
        });
    }, [navigate]);

    return (
        <div>
            <h2>Página Privada</h2>
            <p>{message}</p>
        </div>
    );
}
