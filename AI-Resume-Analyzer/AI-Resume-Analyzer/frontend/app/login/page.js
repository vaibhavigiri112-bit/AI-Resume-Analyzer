"use client";
import {useState} from "react"; import {useRouter} from "next/navigation"; import Link from "next/link";
const API="http://localhost:8000";
export default function Login(){const [email,setEmail]=useState("");const [password,setPassword]=useState("");const [msg,setMsg]=useState("");const router=useRouter();
async function submit(e){e.preventDefault();setMsg("Signing in...");try{const r=await fetch(API+"/api/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,password})});const d=await r.json();if(!r.ok)throw Error(d.detail||"Login failed");localStorage.setItem("token",d.access_token);router.push("/dashboard")}catch(e){setMsg(e.message)}}
return <main className="auth"><form onSubmit={submit} className="card"><h1>Welcome back</h1><p>AI Resume Analyzer</p><input placeholder="Email" type="email" value={email} onChange={e=>setEmail(e.target.value)} required/><input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} required/><button>Login</button><small>{msg}</small><p>New user? <Link href="/register">Create account</Link></p></form></main>}
