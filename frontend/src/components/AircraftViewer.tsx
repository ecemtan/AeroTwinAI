import { useEffect, useRef } from 'react'
import * as THREE from 'three'

/**
 * Three.js viewer skeleton.
 *
 * Scene frame = core/frames.py THREE: +X east, +Y up, +Z south.
 * An aircraft mesh must be authored with its nose along -Z and right wing
 * along +X (BODY_TO_THREE). No Cessna geometry exists yet, so only the frame
 * axes are drawn; nothing here represents the real aircraft.
 */
export function AircraftViewer({ geometryAvailable }: { geometryAvailable: boolean }) {
  const mountRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const mount = mountRef.current
    if (!mount) return

    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200)
    camera.position.set(8, 6, 10)
    camera.lookAt(0, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setPixelRatio(window.devicePixelRatio)
    mount.appendChild(renderer.domElement)

    scene.add(new THREE.GridHelper(20, 20, 0x888888, 0x444444))
    scene.add(new THREE.AxesHelper(4)) // red +X, green +Y (up), blue +Z
    // Arrow showing where an aircraft nose points at heading 0 (north = -Z).
    scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, 0, -1), new THREE.Vector3(0, 0.01, 0), 5, 0xf5a623))

    const resize = () => {
      const width = mount.clientWidth
      const height = mount.clientHeight
      renderer.setSize(width, height, false)
      camera.aspect = width / Math.max(height, 1)
      camera.updateProjectionMatrix()
      renderer.render(scene, camera)
    }
    const observer = new ResizeObserver(resize)
    observer.observe(mount)
    resize()

    return () => {
      observer.disconnect()
      renderer.dispose()
      mount.removeChild(renderer.domElement)
    }
  }, [])

  return (
    <section className="panel">
      <h2>3B görünüm</h2>
      <div className="viewer" ref={mountRef}>
        {!geometryAvailable && (
          <div className="viewer-overlay">
            Cessna 172 3B modeli henüz yok. Yalnızca sahne eksenleri gösteriliyor
            (turuncu ok: burun yönü, kuzey = −Z).
          </div>
        )}
      </div>
    </section>
  )
}
