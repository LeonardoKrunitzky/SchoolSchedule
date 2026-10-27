"use client";

import React, { useState, useEffect } from "react";
import "./schedule.css";
import Navbar from "@/components/navbar/Navbar";
import { getUsers } from "@/services/users";
import {
  getClasses,
  getSchedules,
  createSchedule,
  updateSchedule,
  deleteSchedule,
  ClassRoom,
  ScheduleRecord,
} from "@/services/schedule";

interface User {
  id: string;
  name: string;
}

interface TeacherBlock {
  id: string;
  userId: string;
  teacherName: string;
  color: string;
  classId: string;
  rowId: string;
  startCol: number;
  durationCols: number;
  timeText: string;
  observacao?: string; // <-- Nova propriedade adicionada
}

const DIAS = [
  { label: "Segunda", value: 1 },
  { label: "Terça", value: 2 },
  { label: "Quarta", value: 3 },
  { label: "Quinta", value: 4 },
  { label: "Sexta", value: 5 },
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

function formatTime(timeStr: string): string {
  if (timeStr.includes("T")) {
    return timeStr.split("T")[1].substring(0, 5);
  }
  return timeStr.substring(0, 5);
}

export default function Schedule() {
  const [activeDay, setActiveDay] = useState<number>(DIAS[0].value);
  const [teachers, setTeachers] = useState<User[]>([]);
  const [classes, setClasses] = useState<ClassRoom[]>([]);
  const [teacherColors, setTeacherColors] = useState<Record<string, string>>(
    {},
  );
  const [blocks, setBlocks] = useState<Record<number, TeacherBlock[]>>({});
  const [editingBlock, setEditingBlock] = useState<TeacherBlock | null>(null);

  const loadScheduleData = async () => {
    try {
      const [usersData, classesData, schedulesData] = await Promise.all([
        getUsers(),
        getClasses(),
        getSchedules(),
      ]);

      setTeachers(usersData);
      setClasses(classesData);

      const colors: Record<string, string> = {};
      usersData.forEach((u: User) => {
        colors[u.id] = `hsl(${Math.floor(Math.random() * 360)}, 65%, 88%)`;
      });
      setTeacherColors(colors);

      const userMap = new Map<string, string>(
        usersData.map((u: User) => [u.id, u.name]),
      );
      const classMap = new Map<string, string>(
        classesData.map((c: ClassRoom) => [c.id, c.name]),
      );

      const groupedBlocks: Record<number, TeacherBlock[]> = {};

      schedulesData.forEach(
        (item: ScheduleRecord & { observacao?: string }) => {
          const start = formatTime(item.start_time);
          const end = formatTime(item.end_time);
          const startIndex = Math.max(0, TIMES.indexOf(start));
          const endIndex = Math.max(startIndex + 1, TIMES.indexOf(end));

          const safeTeacherName = userMap.get(item.user_id) ?? "Professor";
          const safeRowId = classMap.get(item.class_id) ?? "";

          const block: TeacherBlock = {
            id: String(item.id),
            userId: String(item.user_id),
            teacherName: safeTeacherName,
            color: colors[item.user_id] || "#e2e8f0",
            classId: String(item.class_id),
            rowId: safeRowId,
            startCol: startIndex + 1,
            durationCols: endIndex - startIndex,
            timeText: `${start} às ${end}`,
            observacao: item.observacao || "", // <-- Resgata do banco caso exista
          };

          if (!groupedBlocks[item.weekday]) {
            groupedBlocks[item.weekday] = [];
          }
          groupedBlocks[item.weekday].push(block);
        },
      );

      setBlocks(groupedBlocks);
    } catch (error) {
      console.error("Failed to load schedule data:", error);
    }
  };

  useEffect(() => {
    loadScheduleData();
  }, []);

  const handleSidebarDragStart = (e: React.DragEvent, teacher: User) => {
    e.dataTransfer.setData("source", "sidebar");
    e.dataTransfer.setData("userId", String(teacher.id));
    e.dataTransfer.setData("teacherName", String(teacher.name));
  };

  const handleGridDragStart = (e: React.DragEvent, blockId: string) => {
    e.dataTransfer.setData("source", "grid");
    e.dataTransfer.setData("blockId", String(blockId));
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = async (
    e: React.DragEvent,
    turma: ClassRoom,
    colIndex: number,
  ) => {
    e.preventDefault();
    const source = e.dataTransfer.getData("source");

    if (source === "sidebar") {
      const userId = e.dataTransfer.getData("userId");
      const teacherName = e.dataTransfer.getData("teacherName");

      if (!userId || !teacherName) return;

      const startTime = TIMES[colIndex] || "07:00";
      const endTime =
        TIMES[Math.min(colIndex + 4, TIMES.length - 1)] || "09:00";

      try {
        const created = await createSchedule({
          user_id: userId,
          class_id: turma.id,
          weekday: activeDay,
          start_time: startTime,
          end_time: endTime,
        });

        const newBlock: TeacherBlock = {
          id: String(created.id),
          userId,
          teacherName,
          color: teacherColors[userId] || "#e2e8f0",
          classId: turma.id,
          rowId: turma.name,
          startCol: colIndex + 1,
          durationCols: 4,
          timeText: `${startTime} às ${endTime}`,
          observacao: "", // <-- Inicia vazio
        };

        setBlocks((prev) => ({
          ...prev,
          [activeDay]: [...(prev[activeDay] || []), newBlock],
        }));
      } catch (error) {
        console.error("Failed to create schedule block:", error);
      }
    } else if (source === "grid") {
      const blockId = e.dataTransfer.getData("blockId");
      const dayBlocks = blocks[activeDay] || [];
      const block = dayBlocks.find((b) => b.id === blockId);

      if (!block) return;

      const newStartCol = colIndex + 1;
      const startTime = TIMES[colIndex] || "07:00";
      const endIndex = Math.min(
        colIndex + block.durationCols,
        TIMES.length - 1,
      );
      const endTime = TIMES[endIndex] || "09:00";

      try {
        await updateSchedule(blockId, {
          user_id: block.userId,
          class_id: turma.id,
          weekday: activeDay,
          start_time: startTime,
          end_time: endTime,
        });

        setBlocks((prev) => ({
          ...prev,
          [activeDay]: (prev[activeDay] || []).map((b) =>
            b.id === blockId
              ? {
                  ...b,
                  classId: turma.id,
                  rowId: turma.name,
                  startCol: newStartCol,
                  timeText: `${startTime} às ${endTime}`,
                }
              : b,
          ),
        }));
      } catch (error) {
        console.error("Failed to move schedule block:", error);
      }
    }
  };

  const saveEdit = async () => {
    if (!editingBlock) return;

    const startSelect = document.getElementById(
      "edit-start",
    ) as HTMLSelectElement;
    const endSelect = document.getElementById("edit-end") as HTMLSelectElement;
    const obsTextarea = document.getElementById(
      "edit-obs",
    ) as HTMLTextAreaElement; // <-- Captura a observação

    const startIndex = TIMES.indexOf(startSelect.value);
    const endIndex = TIMES.indexOf(endSelect.value);
    const newObservacao = obsTextarea ? obsTextarea.value : "";

    if (startIndex >= endIndex) {
      alert("O horário de fim deve ser depois do início.");
      return;
    }

    try {
      await updateSchedule(editingBlock.id, {
        user_id: editingBlock.userId,
        class_id: editingBlock.classId,
        weekday: activeDay,
        start_time: startSelect.value,
        end_time: endSelect.value,
        observacao: newObservacao, // <-- Envia para a API (certifique-se que seu backend aceite essa prop)
      });

      setBlocks((prev) => ({
        ...prev,
        [activeDay]: (prev[activeDay] || []).map((b) =>
          b.id === editingBlock.id
            ? {
                ...b,
                startCol: startIndex + 1,
                durationCols: endIndex - startIndex,
                timeText: `${startSelect.value} às ${endSelect.value}`,
                observacao: newObservacao, // <-- Atualiza o estado local
              }
            : b,
        ),
      }));
      setEditingBlock(null);
    } catch (error) {
      console.error("Failed to update schedule block:", error);
    }
  };

  const deleteBlock = async () => {
    if (!editingBlock) return;

    try {
      await deleteSchedule(editingBlock.id);

      setBlocks((prev) => ({
        ...prev,
        [activeDay]: (prev[activeDay] || []).filter(
          (b) => b.id !== editingBlock.id,
        ),
      }));
      setEditingBlock(null);
    } catch (error) {
      console.error("Failed to delete schedule block:", error);
    }
  };

  const currentDayBlocks = blocks[activeDay] || [];
  const activeDayLabel = DIAS.find((d) => d.value === activeDay)?.label || "";

  return (
    <div className="app-wrapper">
      <Navbar />
      <div className="layout-wrapper">
        <main className="gantt-main">
          <div className="tabs">
            {DIAS.map((dia) => (
              <button
                key={dia.value}
                className={`tab-btn ${activeDay === dia.value ? "active" : ""}`}
                onClick={() => setActiveDay(dia.value)}
              >
                {dia.label}
              </button>
            ))}
          </div>

          <div className="gantt-board">
            <div className="gantt-header">
              <div className="gantt-corner">Turmas</div>
              <div className="gantt-times">
                {TIMES.slice(0, -1).map((t) => (
                  <div key={t} className="time-cell">
                    {t}
                  </div>
                ))}
              </div>
            </div>

            <div className="gantt-body">
              {classes.map((turma) => (
                <div key={turma.id} className="gantt-row">
                  <div className="row-label">{turma.name}</div>
                  <div className="row-grid">
                    {TIMES.slice(0, -1).map((_, idx) => (
                      <div
                        key={idx}
                        className="drop-cell"
                        style={{ gridColumn: idx + 1 }}
                        onDragOver={handleDragOver}
                        onDrop={(e) => handleDrop(e, turma, idx)}
                      />
                    ))}

                    {currentDayBlocks
                      .filter((b) => b.classId === turma.id)
                      .map((block) => (
                        <div
                          key={block.id}
                          className="gantt-block"
                          draggable
                          onDragStart={(e) => handleGridDragStart(e, block.id)}
                          onClick={() => setEditingBlock(block)}
                          style={{
                            backgroundColor: block.color,
                            gridColumn: `${block.startCol} / span ${block.durationCols}`,
                          }}
                        >
                          <strong>{block.teacherName}</strong>
                          <span>{block.timeText}</span>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>

        <aside className="bottom-panel">
          <h3>Educadores</h3>
          <p>
            Arraste o nome do professor para a grade. Clique em um bloco na
            grade para editar o horário ou removê-lo.
          </p>
          <div className="teachers-list">
            {teachers.map((t) => (
              <div
                key={t.id}
                draggable
                onDragStart={(e) => handleSidebarDragStart(e, t)}
                className="teacher-pill"
                style={{ backgroundColor: teacherColors[t.id] || "#eee" }}
              >
                {t.name}
              </div>
            ))}
          </div>
        </aside>

        {editingBlock && (
          <div className="modal-overlay" onClick={() => setEditingBlock(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h3>Editar Aula: {editingBlock.teacherName}</h3>
              <p className="modal-subtitle">
                Turma {editingBlock.rowId} - {activeDayLabel}
              </p>

              <div className="modal-form">
                <div className="input-group">
                  <label>Início</label>
                  <select
                    id="edit-start"
                    defaultValue={editingBlock.timeText.split(" às ")[0]}
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
                    defaultValue={editingBlock.timeText.split(" às ")[1]}
                  >
                    {TIMES.slice(1).map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="input-group full-width">
                  <label>Observação (Opcional)</label>
                  <textarea
                    id="edit-obs"
                    defaultValue={editingBlock.observacao}
                    placeholder="Ex: Trazer material para laboratório..."
                    rows={3}
                  />
                </div>
              </div>

              <div className="modal-actions">
                <button className="btn-delete" onClick={deleteBlock}>
                  Remover da Grade
                </button>
                <div className="modal-actions-right">
                  <button
                    className="btn-cancel"
                    onClick={() => setEditingBlock(null)}
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
