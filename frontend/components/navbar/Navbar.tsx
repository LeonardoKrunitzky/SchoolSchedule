import Link from 'next/link';
import './Navbar.css';
import { AiFillHome } from 'react-icons/ai';
import { FaUsers } from 'react-icons/fa';
import { MdCalendarToday } from 'react-icons/md';
import { BsCalendar2 } from 'react-icons/bs';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="brand">Cronograma Escolar</div>
      <ul className="links">
        <li><Link href="/"><AiFillHome className="nav-icon" />Início</Link></li>
        <li><Link href="/users"><FaUsers className="nav-icon" />Funcionários</Link></li>
        <li><Link href="/schedule"><MdCalendarToday className="nav-icon" />Cronograma</Link></li>
      </ul>
    </nav>
  );
}