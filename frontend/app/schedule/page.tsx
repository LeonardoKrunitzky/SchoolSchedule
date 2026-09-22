"use client";

import React, { useState, useEffect } from "react";
import "./schedule.css";
import Navbar from "@/components/navbar/Navbar";

interface Teacher {
  name: string;
  color: string;
}

interface ScheduleItem {
  id: string;
  teacherName: string;
  time: string;
}

const DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"];
const TURMAS = ["A1", "B1", "C1", "C2", "C3", "D1", "D/E"];
const TEACHERS_NAMES = [
  "Gisele",
  "Nedi",
  "Fabi",
  "Pri",
  "Tielli",
  "Leila",
  "Dacsi",
  "Marceli",
  "Josiane",
  "Tais",
];

const TIMES = [
  "06:00",
  "06:30",
  "07:00",
  "07:30",
  "08:00",
  "08:30",
  "09:00",
  "09:30",
  "10:00",
  "10:30",
  "11:00",
  "11:30",
  "12:00",
  "12:30",
  "13:00",
  "13:30",
  "14:00",
  "14:30",
  "15:00",
  "15:30",
  "16:00",
  "16:30",
  "17:00",
  "17:30",
  "18:00",
];

export default function GradeEscolar() {
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [schedule, setSchedule] = useState<Record<string, ScheduleItem[]>>({});
  const [editingData, setEditingData] = useState<{
    item: ScheduleItem;
    cellKey: string;
  } | null>(null);

  useEffect(() => {
    const generatedTeachers = TEACHERS_NAMES.map((name) => ({
      name,
      color: `hsl(${Math.floor(Math.random() * 360)}, 65%, 85%)`,
    }));
    setTeachers(generatedTeachers);
  }, []);

  const handleSidebarDragStart = (e: React.DragEvent, teacherName: string) => {
    e.dataTransfer.setData("source", "sidebar");
    e.dataTransfer.setData("teacherName", teacherName);
  };

  const handleGridDragStart = (
    e: React.DragEvent,
    sourceKey: string,
    itemId: string,
  ) => {
    e.dataTransfer.setData("source", "grid");
    e.dataTransfer.setData("sourceKey", sourceKey);
    e.dataTransfer.setData("itemId", itemId);
  };

  const handleDragOver = (e: React.DragEvent) => e.preventDefault();

  const handleDrop = (e: React.DragEvent, targetKey: string) => {
    e.preventDefault();
    const source = e.dataTransfer.getData("source");

    if (source === "sidebar") {
      const teacherName = e.dataTransfer.getData("teacherName");
      if (!teacherName) return;

      setSchedule((prev) => ({
        ...prev,
        [targetKey]: [
          ...(prev[targetKey] || []),
          {
            id: Math.random().toString(36).substr(2, 9),
            teacherName,
            time: "07:30 às 09:30",
          },
        ],
      }));
    } else if (source === "grid") {
      const sourceKey = e.dataTransfer.getData("sourceKey");
      const itemId = e.dataTransfer.getData("itemId");
      if (!sourceKey || !itemId) return;

      setSchedule((prev) => {
        const newSchedule = { ...prev };
        let movedItem: ScheduleItem | undefined;

        // Remove do local original
        if (newSchedule[sourceKey]) {
          movedItem = newSchedule[sourceKey].find((i) => i.id === itemId);
          newSchedule[sourceKey] = newSchedule[sourceKey].filter(
            (i) => i.id !== itemId,
          );
        }

        // Adiciona no novo local
        if (movedItem) {
          if (!newSchedule[targetKey]) newSchedule[targetKey] = [];
          newSchedule[targetKey] = [...newSchedule[targetKey], movedItem];
        }

        return newSchedule;
      });
    }
  };

  const getTeacherColor = (name: string) =>
    teachers.find((t) => t.name === name)?.color || "#eee";

  // Modal Actions
  const saveEdit = () => {
    if (!editingData) return;
    const { item, cellKey } = editingData;

    const startSelect = document.getElementById(
      "edit-start",
    ) as HTMLSelectElement;
    const endSelect = document.getElementById("edit-end") as HTMLSelectElement;

    if (TIMES.indexOf(startSelect.value) >= TIMES.indexOf(endSelect.value)) {
      alert("O horário de término deve ser posterior ao início.");
      return;
    }

    const newTime = `${startSelect.value} às ${endSelect.value}`;

    setSchedule((prev) => {
      const newSchedule = { ...prev };
      if (newSchedule[cellKey]) {
        newSchedule[cellKey] = newSchedule[cellKey].map((i) =>
          i.id === item.id ? { ...i, time: newTime } : i,
        );
      }
      return newSchedule;
    });

    setEditingData(null);
  };

  const deleteItem = () => {
    if (!editingData) return;
    const { item, cellKey } = editingData;

    setSchedule((prev) => {
      const newSchedule = { ...prev };
      if (newSchedule[cellKey]) {
        newSchedule[cellKey] = newSchedule[cellKey].filter(
          (i) => i.id !== item.id,
        );
      }
      return newSchedule;
    });
    setEditingData(null);
  };

  return (
    <div className="app-wrapper">
      <Navbar />
      <div className="layout-container">
        <aside className="teachers-sidebar">
          <h2>Educadores</h2>
          <p className="subtitle">Arraste para a grade</p>
          <div className="teachers-list">
            {teachers.map((teacher) => (
              <div
                key={teacher.name}
                draggable
                onDragStart={(e) => handleSidebarDragStart(e, teacher.name)}
                className="teacher-pill"
                style={{ backgroundColor: teacher.color }}
              >
                {teacher.name}
              </div>
            ))}
          </div>
        </aside>

        <main className="schedule-main">
          <div className="grid-container">
            <div className="grid-header-empty">Turmas</div>
            {DIAS.map((dia) => (
              <div key={dia} className="grid-header">
                {dia}
              </div>
            ))}

            {TURMAS.map((turma) => (
              <React.Fragment key={turma}>
                <div className="grid-row-title">{turma}</div>

                {DIAS.map((dia) => {
                  const cellKey = `${turma}-${dia}`;
                  const items = schedule[cellKey] || [];

                  return (
                    <div
                      key={cellKey}
                      className="grid-cell dropzone"
                      onDragOver={handleDragOver}
                      onDrop={(e) => handleDrop(e, cellKey)}
                    >
                      {items.map((item) => (
                        <div
                          key={item.id}
                          draggable
                          onDragStart={(e) =>
                            handleGridDragStart(e, cellKey, item.id)
                          }
                          onClick={() => setEditingData({ item, cellKey })}
                          className="schedule-card"
                          style={{
                            backgroundColor: getTeacherColor(item.teacherName),
                          }}
                        >
                          <strong>{item.teacherName}</strong>
                          <span>{item.time}</span>
                        </div>
                      ))}
                    </div>
                  );
                })}
              </React.Fragment>
            ))}
          </div>
        </main>

        {/* Modal de Edição (Redimensionar / Remover) */}
        {editingData && (
          <div className="modal-overlay" onClick={() => setEditingData(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h3>Editar Aula: {editingData.item.teacherName}</h3>
              <p className="modal-subtitle">
                {editingData.cellKey.split("-")[0]} -{" "}
                {editingData.cellKey.split("-")[1]}
              </p>

              <div className="modal-form">
                <div className="input-group">
                  <label>Início</label>
                  <select
                    id="edit-start"
                    defaultValue={editingData.item.time.split(" às ")[0]}
                  >
                    {TIMES.slice(0, -1).map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="input-group">
                  <label>Fim</label>
                  <select
                    id="edit-end"
                    defaultValue={
                      editingData.item.time.split(" às ")[1] || "09:30"
                    }
                  >
                    {TIMES.slice(1).map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="modal-actions">
                <button className="btn-delete" onClick={deleteItem}>
                  Remover da Grade
                </button>
                <div className="modal-actions-right">
                  <button
                    className="btn-cancel"
                    onClick={() => setEditingData(null)}
                  >
                    Cancelar
                  </button>
                  <button className="btn-save" onClick={saveEdit}>
                    Salvar Horário
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
