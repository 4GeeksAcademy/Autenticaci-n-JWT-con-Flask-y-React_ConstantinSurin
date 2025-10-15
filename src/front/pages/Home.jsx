import React from "react";
import { useNavigate } from "react-router-dom";

export const Home = () => {
	const navigate = useNavigate();

	return (
		<div style={{
			width: "300px",
			margin: "100px auto",
			padding: "20px",
			border: "1px solid #ccc",
			borderRadius: "8px",
			boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
			textAlign: "center",
			backgroundColor: "#f9f9f9"
		}}>
			<h2>Bienvenido</h2>
			<p>Selecciona una opción para continuar:</p>
			<div style={{ display: "flex", justifyContent: "space-around", marginTop: "20px" }}>
				<button
					style={{ padding: "10px 20px", cursor: "pointer" }}
					onClick={() => navigate("/login")}
				>
					Iniciar sesión
				</button>
				<button
					style={{ padding: "10px 20px", cursor: "pointer" }}
					onClick={() => navigate("/signup")}
				>
					Registrarse
				</button>
			</div>
		</div>
	);
};
