"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
export default function Nav(){ const router=useRouter(); const logout=()=>{localStorage.removeItem("token");router.push("/login")}; return <nav><b>AI Resume Analyzer</b><div><Link href="/dashboard">Dashboard</Link><Link href="/upload">Upload Resume</Link><Link href="/jobs">Job Match</Link><button onClick={logout}>Logout</button></div></nav> }
