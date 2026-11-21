import React, { useMemo } from "react";
import { ThreeCanvas } from "@remotion/three";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import * as THREE from "three";

// Toon-shaded coffee beans with an ink outline, so 3D sits inside the hand-drawn craft-book look.
const INK = "#2F2B2A";
const BEAN = "#6B4A33";
const CREASE = "#2A1A10";

const toonRamp = (() => {
  const data = new Uint8Array([90, 170, 255]); // three flat tones = drawn shading
  const tex = new THREE.DataTexture(data, 3, 1, THREE.RedFormat);
  tex.minFilter = THREE.NearestFilter;
  tex.magFilter = THREE.NearestFilter;
  tex.needsUpdate = true;
  return tex;
})();

// a coffee bean: an ellipsoid with one flattened face carrying the crease
function beanGeometry(sx: number, sy: number, sz: number) {
  const g = new THREE.SphereGeometry(1, 96, 96);
  const p = g.attributes.position as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) {
    let z = p.getZ(i);
    if (z > 0.38) z = 0.38 + (z - 0.38) * 0.15; // flat face
    p.setXYZ(i, p.getX(i) * sx, p.getY(i) * sy, z * sz);
  }
  g.computeVertexNormals();
  return g;
}

// crease along the flat face: S-curve for Arabica, nearly straight for Robusta
function creaseGeometry(kind: "arabica" | "robusta", sx: number, sy: number, sz: number) {
  const pts: THREE.Vector3[] = [];
  for (let i = 0; i <= 40; i++) {
    const t = i / 40 - 0.5;
    const x = kind === "arabica" ? Math.sin(t * Math.PI * 2) * 0.28 * sx : 0.03 * sx * Math.sin(t * 6);
    pts.push(new THREE.Vector3(x, t * 1.7 * sy, 0.4 * sz));
  }
  return new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 0.07 * sx, 12, false);
}

const Bean: React.FC<{ kind: "arabica" | "robusta"; x: number; spin: number; tilt: number; scale: number }> = ({ kind, x, spin, tilt, scale }) => {
  const [sx, sy, sz] = kind === "arabica" ? [0.78, 1.18, 0.7] : [0.92, 1.0, 0.72];
  const body = useMemo(() => beanGeometry(sx, sy, sz), [sx, sy, sz]);
  const crease = useMemo(() => creaseGeometry(kind, sx, sy, sz), [kind, sx, sy, sz]);
  return (
    <group position={[x, 0, 0]} rotation={[tilt, spin, kind === "arabica" ? 0.25 : -0.2]} scale={scale}>
      <mesh geometry={body}>
        <meshToonMaterial color={BEAN} gradientMap={toonRamp} />
      </mesh>
      {/* ink outline: inflated back faces */}
      <mesh geometry={body} scale={1.06}>
        <meshBasicMaterial color={INK} side={THREE.BackSide} />
      </mesh>
      <mesh geometry={crease}>
        <meshBasicMaterial color={CREASE} />
      </mesh>
    </group>
  );
};

export const Beans3D: React.FC<{ width: number; height: number; startAt?: number }> = ({ width, height, startAt = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (frame - startAt) / fps;
  const pop = (d: number) => interpolate(frame - startAt, [d, d + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (v) => 1 - (1 - v) ** 3 });
  // turn from the round back to the flat crease side, then keep a slow idle turn
  const spin = (d: number) => interpolate(frame - startAt, [d, d + 40], [Math.PI, 0.35], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (v) => 1 - (1 - v) ** 3 }) + Math.sin(t * 1.2) * 0.25;
  return (
    <ThreeCanvas width={width} height={height} style={{ position: "absolute", left: 0, top: 0 }} camera={{ position: [0, 0, 6], fov: 36 }} gl={{ antialias: true, alpha: true }}>
      <ambientLight intensity={0.55} />
      <directionalLight position={[3, 4, 5]} intensity={1.6} />
      <Bean kind="arabica" x={-1.55} spin={spin(4)} tilt={0.15} scale={pop(4)} />
      <Bean kind="robusta" x={1.55} spin={spin(12)} tilt={0.1} scale={pop(12)} />
    </ThreeCanvas>
  );
};
