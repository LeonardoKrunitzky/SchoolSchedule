import Link from 'next/link';
import './Navbar.css';
import { AiFillHome } from 'react-icons/ai';
import { FaUser, FaUsers } from 'react-icons/fa';
import { MdCalendarToday } from 'react-icons/md';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand">Cronograma Escolar</div>
      <ul className="links">
        <li><Link href="/"><AiFillHome className="nav-icon" />Início</Link></li>
        <li><Link href="/users"><FaUser className="nav-icon" />Funcionários</Link></li>
        <li><Link href="/classes"><FaUsers className="nav-icon" />Turmas</Link></li>
        <li><Link href="/schedule"><MdCalendarToday className="nav-icon" />Cronograma</Link></li>
      </ul>
    </nav>
  );
}